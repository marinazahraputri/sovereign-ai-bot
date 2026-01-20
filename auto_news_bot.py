import asyncio, os, random, requests, subprocess, pickle, time, sys, textwrap, shutil
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# --- ARSITEKTUR V500: THE CRYPTOWAVE OMNIPOTENCE ---
GEMINI_API_KEY = 'AIzaSyBPazkoqLmIjEzcoO1Etnozycq3sroZVH4'
PEXELS_API_KEY = '845Gyp45DUDD9JD8CY7mQyfUaVpG8C73nZED3M0d82thoA0hNR4VzjBQ'
NEWS_API_KEY = '1323151e63ce493f8e0e94353c3a0acc'
FREESOUND_API_KEY = 'RHcVaJy0EhVmOjJWTUAriLfppojg4WmvyIxkiihE'
WATERMARK = "CRYPTOWAVE"

def system_purify():
    for f in ["raw_bg.mp4", "bg_music.mp3", "h1.txt", "h2.txt", "final_wave.mp4"]:
        if os.path.exists(f): os.remove(f)
    os.system("rm -f *.part *.ytdl")

def konsultasi_ai(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    sys_logic = "You are the Head Editor of CRYPTOWAVE. Create explosive, information-rich headlines about specific people or companies. No generic titles. Output ONLY the core text."
    payload = {"contents": [{"parts":[{"text": f"{sys_logic} PROMPT: {prompt}"}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30).json()
        return r['candidates'][0]['content']['parts'][0]['text'].strip()
    except: return None

async def get_cryptowave_news():
    topics = ["crypto investment company news", "billionaire crypto moves", "bitcoin whale alert news", "new financial regulation global"]
    q = random.choice(topics)
    print(f"\n[News]: Membedah sirkuit berita untuk mencari 'Emas'...")
    url = f"https://newsapi.org/v2/everything?q={q}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    
    try:
        res = requests.get(url).json().get('articles', [])
        if not res: return "CRYPTO", "MARKET UPDATE"
        article = random.choice(res)
        title = article['title']
        
        # AI Memaksa ekstraksi Informasi Berbobot (Nama/Peristiwa)
        prompt = (
            f"Based on: {title}. Create two lines for a video. "
            "Line 1 (White): The Name or Main Entity (e.g., ADIK PRABOWO). "
            "Line 2 (Green): The Shocking Action (e.g., TERJUN KE BISNIS CRYPTO). "
            "Be very specific and aggressive. Use Indonesian for high local impact. Format: L1 | L2"
        )
        headlines = konsultasi_ai(prompt)
        if headlines and "|" in headlines:
            h1, h2 = headlines.split("|")
            return h1.strip(), h2.strip()
        return "WHALE ALERT", "MARKET MOVEMENT"
    except: return "GLOBAL", "MARKET NEWS"

async def download_visual(h1):
    headers = {"Authorization": PEXELS_API_KEY}
    v_key = konsultasi_ai(f"Give 1 professional visual keyword (dark office, money, city, luxury) for: {h1}. Word ONLY.") or "finance"
    try:
        res = requests.get(f"https://api.pexels.com/videos/search?query={v_key}&per_page=5&orientation=portrait", headers=headers).json()
        url = random.choice(res['videos'])['video_files'][0]['link']
        with open("raw_bg.mp4", 'wb') as f: f.write(requests.get(url).content)
    except:
        os.system("wget -O raw_bg.mp4 https://www.pexels.com/download/video/3191574/")

async def download_audio():
    # Mencari sound "Investment/Success/Phonk" yang viral
    queries = ["success phonk", "dark cinematic finance", "industrial techno adrenaline"]
    for q in queries:
        try:
            url = f"https://freesound.org/apiv2/search/text/?query={q}&token={FREESOUND_API_KEY}&filter=license:\"Creative Commons 0\"&fields=previews"
            res = requests.get(url).json().get('results', [])
            if res:
                a_url = random.choice(res)['previews']['preview-hq-mp3']
                with open("bg_music.mp3", 'wb') as f: f.write(requests.get(a_url).content)
                return
        except: continue
    os.system("wget -O bg_music.mp3 https://www.soundjay.com/free-music/iron-man-01.mp3")

def render_cryptowave(h1, h2):
    print(f"[Studio]: Merender Masterpiece Cryptowave Style...")
    with open("h1.txt", "w") as f: f.write(textwrap.fill(h1.upper(), width=15))
    with open("h2.txt", "w") as f: f.write(textwrap.fill(h2.upper(), width=18))
    
    # FILTER SUPREME: Layout 3 Tingkat dengan Logo CW_
    f_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "unsharp=5:5:1.5,eq=contrast=1.3:saturation=1.4[v_base];"
        # Bar Hitam Atas & Bawah
        "[v_base]drawbox=y=0:color=black:width=iw:height=300:t=fill[v_bar1];"
        "[v_bar1]drawbox=y=ih-300:color=black:width=iw:height=300:t=fill[v_bar2];"
        # Logo CW_ (Atas & Bawah)
        "[v_bar2]drawtext=text='CW_':fontcolor=white:fontsize=180:x=(w-text_w)/2:y=60[v_logo1];"
        "[v_logo1]drawtext=text='CW_':fontcolor=white:fontsize=180:x=(w-text_w)/2:y=h-240[v_logo2];"
        # Headline Putih (Baris 1)
        "[v_logo2]drawtext=fontfile=font.ttf:textfile=h1.txt:fontcolor=white:fontsize=110:x=(w-text_w)/2:y=(h-text_h)/2-100:shadowcolor=black:shadowx=5:shadowy=5[v1];"
        # Headline HIJAU (Baris 2 - Persis Contoh)
        f"[v1]drawtext=fontfile=font.ttf:textfile=h2.txt:fontcolor=0x00FF00:fontsize=135:x=(w-text_w)/2:y=(h-text_h)/2+180:shadowcolor=black:shadowx=10:shadowy=10,"
        f"drawtext=text='@{WATERMARK}':fontcolor=white@0.3:fontsize=45:x=(w-text_w)/2:y=h-400[v_final]"
    )
    
    cmd = f"ffmpeg -y -i raw_bg.mp4 -stream_loop -1 -i bg_music.mp3 -filter_complex \"{f_complex}\" -map \"[v_final]\" -map 1:a -c:v libx264 -preset superfast -crf 17 -r 60 -t 15 final_wave.mp4"
    os.system(cmd)

def get_youtube():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as t: creds = pickle.load(t)
        if creds and creds.valid: return build('youtube', 'v3', credentials=creds)
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/youtube.upload'])
    creds = flow.run_local_server(port=8080, open_browser=False)
    with open('token.pickle', 'wb') as t: pickle.dump(creds, t)
    return build('youtube', 'v3', credentials=creds)

async def main():
    print("=== THE CRYPTOWAVE V500: THE WORLD IS YOURS ===")
    system_purify()
    youtube = get_youtube()
    
    h1, h2 = await get_cryptowave_news()
    await download_visual(h1)
    await download_audio()
    
    render_cryptowave(h1, h2)
    
    if os.path.exists("final_wave.mp4"):
        judul = f"{h1} {h2} #Shorts #Cryptowave #BillionaireMindset"
        try:
            media = MediaFileUpload("final_wave.mp4", chunksize=-1, resumable=True)
            youtube.videos().insert(part='snippet,status', body={'snippet': {'title': judul[:100], 'categoryId': '25'}, 'status': {'privacyStatus': 'public'}}, media_body=media).execute()
            print("--- 100% SUPREME SUCCESS: MASTERPIECE TAYANG ---")
            system_purify()
        except Exception as e:
            print(f"[Error]: {e}")
            shutil.copy("final_wave.mp4", f"/sdcard/Download/Cryptowave_{random.randint(100,999)}.mp4")
            system_purify()

if __name__ == "__main__":
    asyncio.run(main())
