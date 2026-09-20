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

Gunakan perintah `run_command` pada PowerShell untuk mengeksekusi skrip Python ini.

**Untuk prompt pendek (1 baris):**
Pastikan Anda memformat prompt menjadi **single line** (satu baris lurus tanpa *newline/enter*) agar tidak memicu eror sintaks PowerShell.
```powershell
uv run .agents/scripts/geraikita_query.py --model "NAMA_MODEL_EKSAK" --prompt "ISI PROMPT PENDEK DALAM SATU BARIS"
```

**Untuk prompt panjang / multi-baris / kode / error log:**
Anda dapat menggunakan fitur file sementara (*scratch file*) yang paling aman dari batas karakter PowerShell.
1. Buat file `.txt` atau `.md` sementara (misal di folder `scratch/`).
2. Panggil skrip dengan argumen `--file`:
```powershell
uv run .agents/scripts/geraikita_query.py --model "NAMA_MODEL_EKSAK" --file "path/to/temp.txt"
```
*(Catatan: Skrip Python akan secara otomatis menghapus file sementara tersebut setelah berhasil dieksekusi).*

**Menyimpan output langsung ke file (UTF-8):**
Gunakan `--output-file` untuk menyimpan output langsung ke file tanpa risiko charmap konsol:
```powershell
uv run .agents/scripts/geraikita_query.py --model "NAMA_MODEL_EKSAK" --file "path/to/temp.txt" --output-file "path/to/output.md"
```

Atau alternatifnya (jika tidak menggunakan file), Anda bisa menggunakan fitur `stdin` via Here-Strings PowerShell:
```powershell
@"
Isi prompt yang sangat panjang
bisa terdiri dari banyak baris
"@ | uv run .agents/scripts/geraikita_query.py --model "NAMA_MODEL_EKSAK"
```

Jika Anda ingin melihat daftar lengkap model secara *live*:
```powershell
uv run .agents/scripts/geraikita_query.py --list-models
```
