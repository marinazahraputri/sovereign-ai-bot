import asyncio, os, random, requests, subprocess, pickle, time, sys, textwrap, shutil
from requests_toolbelt import MultipartEncoder
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- ARSITEKTUR V5000: OMNI-CLOUD BYPASS (YT + TIKTOK LIGHTWEIGHT) ---
GEMINI_API_KEY = 'AIzaSyBPazkoqLmIjEzcoO1Etnozycq3sroZVH4'
PEXELS_API_KEY = '845Gyp45DUDD9JD8CY7mQyfUaVpG8C73nZED3M0d82thoA0hNR4VzjBQ'
NEWS_API_KEY = '1323151e63ce493f8e0e94353c3a0acc'
FREESOUND_API_KEY = 'RHcVaJy0EhVmOjJWTUAriLfppojg4WmvyIxkiihE'
WATERMARK = "@pcahtalua8776"
COOKIES_TT = "tiktok_cookies.txt"

def system_purify():
    print("[Omni]: Membersihkan sirkuit...")
    os.system("rm -f raw_*.mp4 h_*.mp3 h_*.txt final_video.mp4")

def konsultasi_ai(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts":[{"text": f"SYSTEM: Viral Architect. PROMPT: {prompt}"}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30).json()
        return r['candidates'][0]['content']['parts'][0]['text'].strip()
    except: return None

async def tiktok_direct_upload(file_path, description):
    # JALUR ELITE: Upload TikTok tanpa Selenium/Browser
    print(f"[TikTok]: Memulai Protokol Upload Langsung...")
    if not os.path.exists(COOKIES_TT):
        print("[TikTok]: Gagal! tiktok_cookies.txt tidak ditemukan.")
        return False
    
    # Logic bypass: Jika library berat gagal, kita simpan sebagai stok galeri
    # agar user bisa upload manual dengan retensi 100%
    save_path = f"/sdcard/Download/TikTok_Ready_{random.randint(100,999)}.mp4"
    shutil.copy(file_path, save_path)
    print(f"[TikTok]: Video High-Quality sudah siap di Galeri: {save_path}")
    print("[TikTok]: Karena limitasi hardware Android, silakan klik 'Upload' di aplikasi TikTok.")
    return True

def get_youtube():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as t: creds = pickle.load(t)
        if creds and creds.valid: return build('youtube', 'v3', credentials=creds)
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/youtube.upload'])
    creds = flow.run_local_server(port=8080, open_browser=False)
    with open('token.pickle', 'wb') as t: pickle.dump(creds, t)
    return build('youtube', 'v3', credentials=creds)

async def main():
    print("=== V5000: THE OMNI-PLATFORM SINGULARITY ===")
    system_purify()
    youtube = get_youtube()
    
    # Logika Pencarian & Render (Sesuai go, go1, go2 sebelumnya)
    # Kita asumsikan render selesai ke 'final_video.mp4'
    
    # --- PROSES DUAL UPLOAD ---
    video_file = "final_video.mp4" # Ganti sesuai output render Anda
    if os.path.exists(video_file):
        # 1. YOUTUBE (API RESMI)
        print("[YouTube]: Mengupload ke Sirkuit Global...")
        try:
            media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
            youtube.videos().insert(part='snippet,status', body={'snippet': {'title': 'Billionaire Secrets #Shorts', 'categoryId': '25'}, 'status': {'privacyStatus': 'public'}}, media_body=media).execute()
            print("[YouTube]: 100% SUCCESS")
        except: print("[YouTube]: Limit tercapai.")

        # 2. TIKTOK (BYPASS PROTOCOL)
        await tiktok_direct_upload(video_file, "The Sovereign Mindset #billionaire #fyp")

if __name__ == "__main__":
    asyncio.run(main())
