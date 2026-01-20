import asyncio, os, random, requests, subprocess, pickle, time, sys, textwrap, shutil
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# --- ARSITEKTUR V600: THE WILDERNESS ARCHITECT ---
GEMINI_API_KEY = 'AIzaSyBPazkoqLmIjEzcoO1Etnozycq3sroZVH4'
PEXELS_API_KEY = '845Gyp45DUDD9JD8CY7mQyfUaVpG8C73nZED3M0d82thoA0hNR4VzjBQ'
FREESOUND_API_KEY = 'RHcVaJy0EhVmOjJWTUAriLfppojg4WmvyIxkiihE'
WATERMARK = "@pcahtalua8776"
HISTORY_FILE = "history_asmr.txt"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def system_purify():
    # Pembersihan agresif untuk memori Android
    os.system("rm -f raw_*.mp4 asmr_*.mp3 h.txt final_asmr.mp4")
    _, _, free = shutil.disk_usage("/")
    print(f"[System]: Memori Tersedia: {free / (2**30):.2f} GB")

def konsultasi_ai(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    sys_logic = "You are a Cinematic Director and Poet. Create short, deep, and peaceful sentences about nature and survival. No emojis. Output ONLY text."
    payload = {"contents": [{"parts":[{"text": f"{sys_logic} PROMPT: {prompt}"}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30).json()
        return r['candidates'][0]['content']['parts'][0]['text'].strip()
    except: return "Peace in the wild."

async def get_sovereign_assets():
    # 1. AI Menentukan Vibe (Danau, Salju, atau Hutan Lebat)
    vibes = ["mountain lake survival", "deep snowy forest shelter", "riverside campfire cabin", "ancient tree house forest"]
    selected_vibe = random.choice(vibes)
    print(f"\n[Oracle]: Memilih Vibe Hari Ini -> {selected_vibe.upper()}")

    # 2. Download 3 Klip 4K (Montage)
    headers = {"Authorization": PEXELS_API_KEY}
    url_v = f"https://api.pexels.com/videos/search?query={selected_vibe}&per_page=15&orientation=portrait"
    v_res = requests.get(url_v, headers=headers).json().get('videos', [])
    
    if len(v_res) < 3:
        v_res = requests.get(f"https://api.pexels.com/videos/search?query=nature survival&orientation=portrait", headers=headers).json().get('videos', [])

    selected_vids = random.sample(v_res, 3)
    v_paths = []
    for i, v in enumerate(selected_vids):
        v_u = v['video_files'][0]['link']
        path = f"raw_{i}.mp4"
        with open(path, 'wb') as f: f.write(requests.get(v_u).content)
        v_paths.append(path)

    # 3. Download Audio ASMR yang Sangat Pas
    print("[Audio]: Mencari suara alam asli...")
    a_query = "forest river" if "lake" in selected_vibe else "snow wind" if "snow" in selected_vibe else "fire crackling"
    url_a = f"https://freesound.org/apiv2/search/text/?query={a_query}&token={FREESOUND_API_KEY}&filter=license:\"Creative Commons 0\"&fields=previews"
    a_res = requests.get(url_a).json().get('results', [])
    a_path = "asmr_final.mp3"
    if a_res:
        a_url = random.choice(a_res)['previews']['preview-hq-mp3']
        with open(a_path, 'wb') as f: f.write(requests.get(a_url).content)
    else: os.system("cp asmr.mp3 asmr_final.mp3")

    # 4. Buat Caption Puitis yang berbeda
    caption = konsultasi_ai(f"Write 1 deep, peaceful sentence about {selected_vibe}. Max 10 words.")
    
    return v_paths, a_path, caption

def render_wilderness(v_paths, a_path, out, caption):
    print(f"[Studio]: Merender Masterpiece Visual 60fps...")
    with open("h.txt", "w") as f: f.write(textwrap.fill(caption.upper(), width=15))
    
    # Filter: Montage 3 klip + Vivid HDR + Vignette + Minimalist Text
    f_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v0];"
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v1];"
        f"[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v2];"
        f"[v0][v1][v2]concat=n=3:v=1:a=0[v_raw];"
        f"[v_raw]unsharp=5:5:1.2,eq=contrast=1.3:saturation=1.5:brightness=-0.02,vignette=angle=0.5[v_fin];"
        f"[v_fin]drawtext=fontfile=font.ttf:textfile=h.txt:fontcolor=white@0.8:fontsize=70:x=(w-text_w)/2:y=(h-text_h)/2:shadowcolor=black:shadowx=4:shadowy=4,"
        f"drawtext=text='{WATERMARK}':fontcolor=white@0.2:fontsize=40:x=(w-text_w)/2:y=h-200[v_out]"
    )
    
    cmd = f"ffmpeg -y -i {v_paths[0]} -i {v_paths[1]} -i {v_paths[2]} -stream_loop -1 -i {a_path} -filter_complex \"{f_complex}\" -map \"[v_out]\" -map 3:a -c:v libx264 -preset superfast -crf 18 -r 60 -t 58 {out}"
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
    print("=== THE WILDERNESS ARCHITECT V600 ONLINE ===")
    system_purify()
    youtube = get_youtube()
    
    v_paths, a_path, caption = await get_sovereign_assets()
    output_name = f"Wilderness_{random.randint(100,999)}.mp4"
    
    render_wilderness(v_paths, a_path, output_name, caption)
    
    if os.path.exists(output_name):
        judul_yt = f"Satisfying Survival ASMR: {caption} #nature #asmr #survival"
        try:
            print(f"[YouTube]: Mengupload Mahakarya Alam...")
            media = MediaFileUpload(output_name, chunksize=-1, resumable=True)
            youtube.videos().insert(part='snippet,status', body={'snippet': {'title': judul_yt[:100], 'categoryId': '10'}, 'status': {'privacyStatus': 'public'}}, media_body=media).execute()
            print("--- 100% SUCCESS: NATURE SINGULARITY TAYANG ---")
            system_purify()
        except Exception as e:
            shutil.copy(output_name, f"/sdcard/Download/{output_name}")
            print(f"[Limit]: Tersimpan di Galeri HP.")
            system_purify()

if __name__ == "__main__":
    asyncio.run(main())
