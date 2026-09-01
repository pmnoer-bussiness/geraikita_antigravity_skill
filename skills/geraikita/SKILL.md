---
name: geraikita
description: Memungkinkan agen untuk bertanya atau mendelegasikan tugas kepada model-model pihak ketiga di Geraikita AI (Claude, Deepseek, GPT, dll). Gunakan skill ini jika pengguna secara eksplisit meminta Anda menggunakan model tertentu (seperti Claude, GPT, Deepseek, Qwen) untuk tugas tertentu.
---

# Skill: geraikita

Skill ini membekali Anda dengan kemampuan untuk mengirim prompt ke API eksternal Geraikita yang menyediakan berbagai model unggulan.

## Daftar Model yang Didukung

Berikut adalah *exact model names* yang wajib Anda gunakan sebagai argumen `--model`. Jika pengguna menggunakan sebutan santai (contoh: "tanyakan ke claude sonnet"), Anda HARUS mencocokkannya ke salah satu ID di bawah ini secara logis (contoh: `claude-sonnet-5`).

**Claude 3.5 / 3 (Anthropic):**
- `claude-sonnet-5` (Claude 3.5 Sonnet)
- `claude-opus-5` (Claude 3.5 Opus)
- `claude-haiku-4-5`
- `claude-sonnet-5-thinking`
- `claude-opus-5-thinking`
- (Serta varian `-authentic`)

**DeepSeek:**
- `deepseek-v4-pro`
- `deepseek-v4-flash`

**GPT-4 / GPT-4o (OpenAI):**
- `gpt-5.5`
- `gpt-5.6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`
- (Serta varian `-authentic`)

**Qwen (Alibaba):**
- `qwen-max`, `qwen-plus`, `qwen-flash`, `qwen-coder-plus`

**Lainnya:**
- `glm-5.1`, `glm-5-turbo`, `glm-5.3`, `glm-5.2`
- `kimi-k2.7-code`, `kimi-k3`

## Cara Menggunakan (Execution)

Gunakan perintah `run_command` pada PowerShell untuk mengeksekusi skrip Python ini. Anda bertugas merangkai *prompt* yang baik berdasarkan permintaan pengguna, lalu memanggil skrip:

```powershell
uv run .agents/scripts/geraikita_query.py --model "NAMA_MODEL_EKSAK" --prompt "ISI_PROMPT_ANDA"
```

Jika Anda ingin melihat daftar lengkap model secara *live*:
```powershell
uv run .agents/scripts/geraikita_query.py --list-models
```
