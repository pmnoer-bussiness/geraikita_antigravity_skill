# Geraikita AI Antigravity Skill

Repositari ini berisi kustomisasi (Skill) untuk **Google Antigravity** yang memungkinkan agen AI Anda untuk berinteraksi dengan API premium dari [Geraikita AI](https://ai.geraikita.com).

Dengan skill ini, Antigravity dapat mendelegasikan tugas atau meminta bantuan (opini kedua) dari 30+ model LLM unggulan seperti:
- Claude 3.5 Sonnet & Opus
- DeepSeek V4 (Pro/Flash)
- GPT-4o (Luna/Sol/Terra)
- Qwen, GLM, dan Kimi

Antigravity juga dapat diperankan sebagai Orkestrator dalam memanage multiple agent dengan LLM yang berbeda (mirip /teamwork-preview, namun menggunakan external LLM Model).

Contoh prompting:
"Tolong buatkan website dinamis untuk profile perusahaan PT. Wadidaw. Gunakan /geraikita dengan ketentuan berikut:
1. Opus-5-Thinking untuk perencanaa.
2. Deepseek 4 Pro untuk coding.
3. Sonnet-5-Thinking untuk mengaudit kode."

## 🚀 Cara Instalasi

1. **Clone ke dalam proyek Anda:**
   Buka terminal di dalam root proyek Antigravity Anda, lalu jalankan:
   ```bash
   git clone https://github.com/pmnoer-bussiness/geraikita_antigravity_skill.git .agents
   ```
   *(Catatan: Jika Anda sudah memiliki folder `.agents`, Anda dapat menyalin folder `scripts` dan `skills` dari repo ini ke dalamnya).*

2. **Atur API Key:**
   Skill ini membutuhkan API Key dari Geraikita. Anda WAJIB menyimpannya sebagai *environment variable* bernama `GERAIKITA_API_KEY`.
   - **Windows:** Tambahkan melalui *Environment Variables* di Control Panel/Settings.
   - **Linux/Mac:** Tambahkan `export GERAIKITA_API_KEY="gk-xxxx"` ke `~/.bashrc` atau `~/.zshrc`.
   
   *Jangan lupa untuk me-restart Antigravity setelah mengatur variabel ini.*

3. **Prasyarat Dependensi (Otomatis):**
   Skrip di dalam repo ini menggunakan `uv run` dan *PEP 723 inline metadata*. Ini berarti selama [uv](https://github.com/astral-sh/uv) terinstal di sistem Anda, pustaka `openai` akan diunduh secara otomatis dan terisolasi tanpa mengotori *environment* Python global Anda!

## 💡 Cara Penggunaan

Setelah terinstal, agen Antigravity akan otomatis mempelajari daftar lengkap model yang didukung. Anda cukup memintanya menggunakan bahasa sehari-hari secara natural di dalam chat:

- *"Tolong cek kode saya ini, coba gunakan geraikita model claude sonnet 5."*
- *"Gunakan geraikita deepseek pro untuk membuat draf email ini."*
- *"Tanya ke geraikita pakai gpt 5.5: apa itu Model Context Protocol?"*

Atau Anda juga bisa memaksanya melalui *slash command* bayangan:
- `/geraikita claude sonnet 5: Tolong review kode saya ini.`

## 🛠️ Struktur Folder
- `scripts/geraikita_query.py`: Skrip utama yang menjembatani Antigravity dengan API Geraikita (kompatibel dengan format OpenAI).
- `skills/geraikita/SKILL.md`: Instruksi internal (*prompt*) agar agen AI tahu cara menggunakan skrip tersebut beserta daftar lengkap ID modelnya.

---
*Dibuat oleh kolaborasi PMNoer Business & Google Antigravity AI.*
