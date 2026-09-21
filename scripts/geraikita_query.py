# /// script
# dependencies = [
#     "openai",
# ]
# ///

import argparse
import os
import sys
import io
import time
from openai import OpenAI, APIConnectionError, APITimeoutError, InternalServerError

# 1. Solusi Anti-Charmap: Paksa encoding UTF-8 pada stdout dan stderr dengan error handler 'replace'
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Daftar model statis (diambil dari https://ai.geraikita.com/en/docs#model)
AVAILABLE_MODELS = [
    "claude-opus-5", "claude-opus-4-8", "claude-opus-4-6", "claude-opus-4-7",
    "claude-sonnet-5", "claude-sonnet-4-6", "claude-haiku-4-5", "claude-fable-5",
    "deepseek-v4-pro", "deepseek-v4-flash",
    "claude-opus-5-thinking", "claude-sonnet-5-thinking",
    "glm-5.1", "glm-5-turbo", "glm-5.3", "glm-5.2",
    "gpt-5.4", "gpt-5.5", "gpt-5.5-xhigh", "gpt-5.6-luna", "gpt-5.6-sol", "gpt-5.6-terra",
    "qwen-max", "qwen-plus", "qwen-flash", "qwen-coder-plus",
    "kimi-k2.7-code", "kimi-k3",
    "claude-opus-5-authentic", "claude-opus-4-8-authentic", "claude-opus-4-7-authentic", "claude-opus-4-6-authentic",
    "claude-sonnet-5-authentic", "claude-sonnet-4-6-authentic", "claude-haiku-4-5-authentic",
    "gpt-5.6-sol-authentic", "gpt-5.6-terra-authentic", "gpt-5.6-luna-authentic", "gpt-5.5-authentic"
]

def list_models():
    print("Available Geraikita AI Models:")
    print("-" * 30)
    for model in AVAILABLE_MODELS:
        print(f"- {model}")
    print("-" * 30)

def main():
    parser = argparse.ArgumentParser(description="Query Geraikita AI models with auto-retry and resilient streaming")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--model", type=str, help="The exact model name to use")
    parser.add_argument("--prompt", type=str, help="The prompt to send to the model (optional if piped via stdin or --file is used)")
    parser.add_argument("--file", type=str, help="Path to a text file containing the prompt")
    parser.add_argument("--output-file", type=str, help="Optional path to save full response directly to a file in UTF-8")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming for faster round-trip on short prompts")
    parser.add_argument("--progress-interval", type=int, default=300, help="Interval in seconds for logging progress heartbeat when writing to --output-file (default: 300s = 5m)")

    args = parser.parse_args()

    if args.list_models:
        list_models()
        return

    if not args.model:
        parser.print_help()
        sys.exit(1)

    prompt_text = args.prompt
    file_to_cleanup = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                prompt_text = f.read().strip()
            file_to_cleanup = args.file
        except Exception as e:
            print(f"Error reading prompt file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    elif not prompt_text:
        # Read from stdin if --prompt or --file is not provided
        if not sys.stdin.isatty():
            prompt_text = sys.stdin.read().strip()

    if not prompt_text:
        print("Error: No prompt provided. Use --prompt, --file, or pipe text via stdin.", file=sys.stderr)
        sys.exit(1)

    if args.model not in AVAILABLE_MODELS:
        print(f"Warning: Model '{args.model}' is not in the known list of models. The API might return 404.", file=sys.stderr)

    api_key = os.environ.get("GERAIKITA_API_KEY")
    if not api_key:
        print("Error: GERAIKITA_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it in your Windows Environment Variables or .env.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        base_url="https://ai.geraikita.com/v1",
        api_key=api_key,
        timeout=180.0,
        max_retries=2
    )

    out_file_handle = None
    if args.output_file:
        try:
            out_file_handle = open(args.output_file, 'w', encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not open output file {args.output_file}: {e}", file=sys.stderr)

    # Auto-Retry Loop (Hingga 3x jika koneksi drop / remote disconnected)
    max_retries = 3
    success = False

    for attempt in range(1, max_retries + 1):
        try:
            if args.no_stream:
                response = client.chat.completions.create(
                    model=args.model,
                    messages=[{"role": "user", "content": prompt_text}],
                    stream=False
                )
                content = response.choices[0].message.content or ""
                sys.stdout.write(content)
                sys.stdout.write("\n")
                sys.stdout.flush()
                if out_file_handle:
                    out_file_handle.write(content)
                    out_file_handle.flush()
            else:
                response = client.chat.completions.create(
                    model=args.model,
                    messages=[{"role": "user", "content": prompt_text}],
                    stream=True
                )
                
                start_time = time.time()
                last_progress_time = start_time
                total_chars = 0
                total_bytes = 0

                for chunk in response:
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            sys.stdout.write(content)
                            sys.stdout.flush()
                            total_chars += len(content)
                            total_bytes += len(content.encode('utf-8', errors='replace'))

                            if out_file_handle:
                                out_file_handle.write(content)
                                out_file_handle.flush()

                            now = time.time()
                            if (now - last_progress_time) >= args.progress_interval:
                                last_progress_time = now
                                elapsed_min = int((now - start_time) / 60)
                                dest = args.output_file if args.output_file else "stdout"
                                sys.stderr.write(
                                    f"\n[GERAIKITA PROGRESS] {elapsed_min}m elapsed | Written {total_chars:,} chars ({total_bytes / 1024:.1f} KB) to {dest}...\n"
                                )
                                sys.stderr.flush()
                print() # Newline at the end

            success = True
            break
        except (APIConnectionError, APITimeoutError, InternalServerError, ConnectionResetError, Exception) as e:
            err_str = str(e)
            if attempt < max_retries:
                backoff = attempt * 2
                print(f"\n[GERAIKITA WARNING] Attempt {attempt} failed ({err_str}). Retrying in {backoff}s...", file=sys.stderr)
                time.sleep(backoff)
            else:
                print(f"\n[GERAIKITA ERROR] All {max_retries} attempts failed: {err_str}", file=sys.stderr)
                sys.exit(1)
        finally:
            pass

    if out_file_handle:
        out_file_handle.close()

    # Hapus file prompt sementara hanya jika eksekusi benar-benar sukses
    if success and file_to_cleanup and os.path.exists(file_to_cleanup):
        try:
            os.remove(file_to_cleanup)
        except Exception:
            pass

if __name__ == "__main__":
    main()
