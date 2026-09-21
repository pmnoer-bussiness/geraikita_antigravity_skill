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

Skrip mendukung fallback lokasi otomatis:
- Workspace: `.agents/scripts/geraikita_query.py`
- Global: `C:\Users\user\.gemini\config\scripts\geraikita_query.py`

### Panduan 3 Kategori Prompt & Aturan Eksekusi:

Agen **WAJIB** mengklasifikasikan prompt ke dalam 3 kategori sebelum memanggil skrip:

---

### Kategori 1: Prompt Pendek (< 100 kata / < 500 karakter)
Digunakan untuk pertanyaan cepat, definisi singkat, atau instruksi ringkas 1 baris.
* **Mode Streaming:** Gunakan `--no-stream` agar latensi round-trip lebih instan.
* **Format Prompt:** Gunakan argumen `--prompt "ISI PROMPT SINGLE LINE"` (satu baris tanpa enter).
* **Output:** Cukup ke stdout konsol (tidak wajib `--output-file`).
```powershell
uv run .agents/scripts/geraikita_query.py --model "claude-sonnet-5" --prompt "Jelaskan ringkas apa itu Stellar Soroban." --no-stream
```

---

### Kategori 2: Prompt Menengah (100–500 kata / 500–2.500 karakter)
Digunakan untuk analisis modular, review fungsi tunggal, atau penjelasan teknis multi-paragraf.
* **Mode Streaming:** Wajib `stream=True` (default tanpa `--no-stream`).
* **Sistem Buffer Input:** Tulis prompt ke file sementara di folder `scratch/`, oper via `--file`.
* **Output:** **SELALU TERAPKAN `--output-file`** untuk menyimpan hasil lengkap dalam UTF-8 tanpa terpotong batas konsol.
```powershell
# 1. Tulis prompt ke scratch buffer
# 2. Eksekusi dengan --file dan --output-file:
uv run .agents/scripts/geraikita_query.py --model "claude-sonnet-5" --file "scratch/prompt_mid.txt" --output-file "scratch/output_mid.md"
```
*(Catatan: File prompt `scratch/prompt_mid.txt` otomatis dihapus oleh skrip saat eksekusi berhasil).*

---

### Kategori 3: Prompt Panjang (> 500 kata / > 2.500 karakter / Audit Kode Penuh)
Digunakan untuk audit keamanan menyeluruh, refactoring arsitektur besar, atau input teks/log yang sangat masif.
* **Mode Streaming:** Wajib `stream=True` (default).
* **Sistem Buffer Input:** Wajib via scratch file buffer (`--file "scratch/prompt_large.txt"`).
* **Output:** **SELALU TERAPKAN `--output-file`**.
* **Pengawasan 2 Lapis (Wajib Setiap 5 Menit):**
  1. **Lapis 1 (Internal Skrip Python):**
     Skrip secara otomatis mencetak log detak jantung (*heartbeat*) ke `stderr` setiap 5 menit (300 detik) yang melaporkan jumlah karakter dan ukuran byte yang sudah tertulis ke file output:
     `[GERAIKITA PROGRESS] 5m elapsed | Written 24,500 chars (24.2 KB) to scratch/audit_output.md...`
  2. **Lapis 2 (Eksternal Asisten Agen):**
     - Agen mengeksekusi perintah menggunakan `run_command`. Karena memakan waktu beberapa menit, perintah akan otomatis berjalan di latar belakang (*background task*).
     - Agen **WAJIB** menjadwalkan pengecekan panjang file output secara berkala setiap 5 menit (misal menggunakan tool `schedule` atau memeriksa `(Get-Item <output_file>).Length`).
     - Jika ukuran file bertambah $\to$ proses generasi berjalan sehat dan lancar.
     - Jika ukuran file tidak bertambah sama sekali selama > 10 menit $\to$ deteksi potensi koneksi terputus dan tangani segera.

Contoh Eksekusi Prompt Panjang:
```powershell
uv run .agents/scripts/geraikita_query.py --model "claude-opus-5" --file "scratch/audit_prompt.txt" --output-file "scratch/audit_report.md" --progress-interval 300
```

---

### Utilitas Tambahan
Melihat daftar lengkap model secara *live*:
```powershell
uv run .agents/scripts/geraikita_query.py --list-models
```

