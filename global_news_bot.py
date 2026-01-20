import asyncio, os, random, requests, subprocess, pickle, time, sys, textwrap, shutil
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# --- ARSITEKTUR V1000: THE GLOBAL NEWS ORACLE (100% PERFECT) ---
GEMINI_API_KEY = 'AIzaSyBPazkoqLmIjEzcoO1Etnozycq3sroZVH4'
PEXELS_API_KEY = '845Gyp45DUDD9JD8CY7mQyfUaVpG8C73nZED3M0d82thoA0hNR4VzjBQ'
NEWS_API_KEY = '1323151e63ce493f8e0e94353c3a0acc'
FREESOUND_API_KEY = 'RHcVaJy0EhVmOjJWTUAriLfppojg4WmvyIxkiihE'
WATERMARK = "NEWS GLOBAL"
HISTORY_FILE = "history_global_news.txt"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def system_purify():
    print("[System]: Purifikasi jalur sirkuit global...")
    junk = ["raw_bg.mp4", "bg_music.mp3", "h_w.txt", "h_g.txt", "final_global.mp4"]
    for f in junk:
        if os.path.exists(f): os.remove(f)
    os.system("rm -f *.part *.ytdl")
    total, used, free = shutil.disk_usage("/")
    print(f"[System]: Memori Aman: {free / (2**30):.2f} GB")

def konsultasi_ai(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    sys_logic = "You are the Head Editor of NEWS GLOBAL. You have access to 1 trillion data points. Create explosive, factual, and adrenaline-pumping world news headlines. NO HOAX. Output ONLY the requested format."
    payload = {"contents": [{"parts":[{"text": f"{sys_logic} PROMPT: {prompt}"}]}]}
    try:
        r = requests.post(url, json=payload, timeout=35).json()
        if 'candidates' in r and len(r['candidates']) > 0:
            return r['candidates'][0]['content']['parts'][0]['text'].strip()
    except: pass
    return None

async def get_world_news():
    # Daftar pencarian berita global paling panas dan berdampak
    queries = [
        "US CPI inflation data result today",
        "Donald Trump Greenland policy plan",
        "Venezuela president Maduro incident news",
        "Palestine conflict latest update today",
        "Indonesia government meeting result",
        "World Economic Forum global crisis"
    ]
    q = random.choice(queries)
    print(f"\n[Oracle]: Memindai ribuan media untuk berita: {q}...")
    
    url = f"https://newsapi.org/v2/everything?q={q}&language=en&sortBy=publishedAt&pageSize=15&apiKey={NEWS_API_KEY}"
    res = requests.get(url).json().get('articles', [])
    used = open(HISTORY_FILE).read().splitlines() if os.path.exists(HISTORY_FILE) else []
    
    # Ambil berita yang belum pernah digunakan dan valid
    article = next((a for a in res if a['title'] not in used and len(a['title']) > 20), res[0] if res else None)
    
    if not article:
        return "WORLD NEWS", "UPDATE TODAY", "No specific news found"

    title = article['title']
    
    # AI Memecah Berita menjadi Headline Sempurna (STYLE: NEWS GLOBAL)
    prompt = (
        f"Based on this news: {title}. Split into two lines. "
        "Line 1: The Subject/Location (White). "
        "Line 2: The Action/Shocking Result (Neon Green). "
        "Use Indonesian for local impact. Make it extremely urgent and dramatic. "
        "Example: HASIL RAPAT AMERIKA | EKONOMI DUNIA TERANCAM. Format: L1 | L2"
    )
    result = konsultasi_ai(prompt)
    if result and "|" in result:
        h_w, h_g = result.split("|")[0].strip(), result.split("|")[1].strip()
        with open(HISTORY_FILE, "a") as f: f.write(title + "\n")
        return h_w, h_g, title
    return "BERITA GLOBAL", "UPDATE TERBARU", title

async def download_assets(h_w):
    # 1. Visual 4K Sinematik dari Pexels
    headers = {"Authorization": PEXELS_API_KEY}
    v_key = konsultasi_ai(f"Give 1 keyword for global news visual (city, military, technology, gold) based on: {h_w}. Word ONLY.") or "global"
    print(f"[Visual]: Mencari latar belakang sinematik: {v_key}...")
    try:
        r_v = requests.get(f"https://api.pexels.com/videos/search?query={v_key}&per_page=10&orientation=portrait", headers=headers).json()
        v_url = random.choice(r_v['videos'])['video_files'][0]['link']
        with open("raw_bg.mp4", 'wb') as f: f.write(requests.get(v_url).content)
    except:
        os.system("wget -O raw_bg.mp4 https://www.pexels.com/download/video/3191574/")
    
    # 2. Audio Adrenalin dari Freesound (Anti-Empty-Sequence)
    print("[Audio]: Mengambil musik pengguncang adrenalin...")
    queries = ["industrial dark", "phonk aggressive", "cinematic tension"]
    for aq in queries:
        try:
            url_a = f"https://freesound.org/apiv2/search/text/?query={aq}&token={FREESOUND_API_KEY}&filter=license:\"Creative Commons 0\"&fields=previews"
            res_a = requests.get(url_a).json().get('results', [])
            if res_a:
                a_url = random.choice(res_a)['previews']['preview-hq-mp3']
                with open("bg_music.mp3", 'wb') as f: f.write(requests.get(a_url).content)
                return
        except: continue
    os.system("wget -O bg_music.mp3 https://www.soundjay.com/free-music/iron-man-01.mp3")

def render_global_oracle(h_w, h_g):
    print(f"[Studio]: Merender Mahakarya NEWS GLOBAL 60fps...")
    with open("h_w.txt", "w") as f: f.write(textwrap.fill(h_w.upper(), width=15))
    with open("h_g.txt", "w") as f: f.write(textwrap.fill(h_g.upper(), width=15))
    
    # FILTER V1000: HDR Vivid, High Contrast, Dual Layer Teks (Putih & Hijau)
    f_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "unsharp=5:5:1.5,eq=contrast=1.4:saturation=1.6:brightness=-0.05[base];"
        "[base]drawbox=y=ih/2-400:color=black@0.6:width=iw:height=800:t=fill[sh];"
        "[sh]drawtext=fontfile=font.ttf:textfile=h_w.txt:fontcolor=white:fontsize=120:x=(w-text_w)/2:y=(h-text_h)/2-180:shadowcolor=black:shadowx=5:shadowy=5[v1];"
        f"[v1]drawtext=fontfile=font.ttf:textfile=h_g.txt:fontcolor=0x00FF00:fontsize=145:x=(w-text_w)/2:y=(h-text_h)/2+220:shadowcolor=black:shadowx=10:shadowy=10,"
        f"drawtext=text='{WATERMARK}':fontcolor=white@0.5:fontsize=55:x=(w-text_w)/2:y=h-250[v_out]"
    )
    
    cmd = f"ffmpeg -y -i raw_bg.mp4 -stream_loop -1 -i bg_music.mp3 -filter_complex \"{f_complex}\" -map \"[v_out]\" -map 1:a -c:v libx264 -preset superfast -crf 17 -r 60 -t 15 final_global.mp4"
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
    print("\n" + "!"*50 + "\n   V1000: GLOBAL NEWS ORACLE ACTIVATED\n" + "!"*50)
    system_purify()
    
    # Pastikan Font Ada
    if not os.path.exists("font.ttf"):
        os.system("wget -O font.ttf 'https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf'")

    youtube = get_youtube()
    
    h_w, h_g, original_title = await get_world_news()
    await download_assets(h_w)
    
    render_global_oracle(h_w, h_g)
    
    if os.path.exists("final_global.mp4"):
        judul_yt = f"{h_w} {h_g} #BreakingNews #WorldUpdate #Shorts"
        try:
            print("[YouTube]: Mengirim Berita Global ke Seluruh Dunia...")
            media = MediaFileUpload("final_global.mp4", chunksize=-1, resumable=True)
            youtube.videos().insert(part='snippet,status', body={'snippet': {'title': judul_yt[:100], 'categoryId': '25'}, 'status': {'privacyStatus': 'public'}}, media_body=media).execute()
            print("--- 1000% SUCCESS: WORLD HAS BEEN INFORMED ---")
            system_purify()
        except Exception as e:
            shutil.copy("final_global.mp4", f"/sdcard/Download/News_{random.randint(100,999)}.mp4")
            print(f"[Limit]: Video disimpan ke Galeri HP.")
            system_purify()

if __name__ == "__main__":
    asyncio.run(main())
