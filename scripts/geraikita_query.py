# /// script
# dependencies = [
#     "openai",
# ]
# ///

import argparse
import os
import sys
import io
from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
    parser = argparse.ArgumentParser(description="Query Geraikita AI models")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--model", type=str, help="The exact model name to use")
    parser.add_argument("--prompt", type=str, help="The prompt to send to the model")

    args = parser.parse_args()

    if args.list_models:
        list_models()
        return

    if not args.model or not args.prompt:
        parser.print_help()
        sys.exit(1)

    if args.model not in AVAILABLE_MODELS:
        print(f"Warning: Model '{args.model}' is not in the known list of models. The API might return 404.", file=sys.stderr)

    api_key = os.environ.get("GERAIKITA_API_KEY")
    if not api_key:
        print("Error: GERAIKITA_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it in your Windows Environment Variables or .env.", file=sys.stderr)
        sys.exit(1)

    try:
        client = OpenAI(
            base_url="https://ai.geraikita.com/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": args.prompt}],
        )
        
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error querying API: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
