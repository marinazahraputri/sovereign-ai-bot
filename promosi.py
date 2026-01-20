import asyncio
import edge_tts

# Teks yang sudah dioptimalkan untuk intonasi profesional
TEXT = """
Banyak orang gagal di YouTube karena satu hal: Gak konsisten. 
Ngedit video kualitas empat ka itu lama dan sangat menguras tenaga. 
Gue gak mau terjebak di sana, makanya gue ngerakit sebuah sistem.

Ini adalah Autonomous AI Studio yang jalan langsung di Termux handphone gue. 
Otaknya menggunakan Gemini AI, dia membedah data global secara real-time. 
Visualnya empat ka dari Pexels, audionya dari Freesound. 
Semuanya seratus persen otomatis, dari riset sampai proses upload.

Target gue bukan lokal, tapi Global. 
Semua konten menggunakan Bahasa Inggris untuk mendapatkan penghasilan Dollar. 
Sistem ini kerja dua puluh empat jam buat bangun aset digital gue, bahkan saat gue lagi tidur.

Gue buka akses buat lo yang paham konsep leverage dan mau punya sistem serupa di Android lo. 
DM gue ARCHITECT, gue tunjukin cara ngerakitnya. 
Take action sekarang.
"""

# Menggunakan suara id-ID-ArdiNeural (Pria, Tegas, Profesional)
VOICE = "id-ID-ArdiNeural"
OUTPUT_FILE = "suara_promosi.mp3"

async def generate_voice():
    print(f"Sedang menghasilkan suara AI profesional...")
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="+0%", pitch="+0Hz")
    await communicate.save(OUTPUT_FILE)
    print(f"Berhasil! File tersimpan sebagai: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_voice())
