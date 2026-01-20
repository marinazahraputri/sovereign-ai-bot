import asyncio, os, random, requests, subprocess, pickle, time, sys, textwrap, shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

GEMINI_API_KEY = 'AIzaSyBPazkoqLmIjEzcoO1Etnozycq3sroZVH4'
PEXELS_API_KEY = '845Gyp45DUDD9JD8CY7mQyfUaVpG8C73nZED3M0d82thoA0hNR4VzjBQ'
NEWS_API_KEY = '1323151e63ce493f8e0e94353c3a0acc'
FREESOUND_API_KEY = 'RHcVaJy0EhVmOjJWTUAriLfppojg4WmvyIxkiihE'
WATERMARK = "TOBEHUMAN1%"

def konsultasi_ai(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts":[{"text": f"SYSTEM: Professional News Editor. Format: L1 | L2. PROMPT: {prompt}"}]}]}
    try:
        r = requests.post(url, json=payload).json()
        return r['candidates'][0]['content']['parts'][0]['text'].strip()
    except: return "MARKET | UPDATE"

async def main():
    print("=== CRYPTO ENGINE: TOBEHUMAN1% ===")
    n_res = requests.get(f"https://newsapi.org/v2/everything?q=bitcoin&language=en&apiKey={NEWS_API_KEY}").json()
    title = n_res['articles'][0]['title']
    res_ai = konsultasi_ai(f"Split this news into 2 aggressive lines (L1: White, L2: Green): {title}")
    h_w, h_g = res_ai.split("|") if "|" in res_ai else ("MARKET", "ALERT")

    v_res = requests.get(f"https://api.pexels.com/videos/search?query=finance&per_page=5&orientation=portrait", headers={"Authorization": PEXELS_API_KEY}).json()
    v_url = random.choice(v_res['videos'])['video_files'][0]['link']
    with open("raw.mp4", 'wb') as f: f.write(requests.get(v_url).content)
    os.system(f"wget -O music.mp3 https://www.soundjay.com/free-music/designing-future-01.mp3")

    f_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "unsharp=5:5:1.5,eq=contrast=1.4:saturation=1.6[base];"
        "[base]drawbox=y=ih/2-400:color=black@0.5:width=iw:height=800:t=fill[sh];"
        f"[sh]drawtext=fontfile=font.ttf:text='{h_w.upper()}':fontcolor=white:fontsize=120:x=(w-text_w)/2:y=(h-text_h)/2-180[v1];"
        f"[v1]drawtext=fontfile=font.ttf:text='{h_g.upper()}':fontcolor=0x00FF00:fontsize=145:x=(w-text_w)/2:y=(h-text_h)/2+220[v2];"
        f"[v2]drawtext=text='{WATERMARK}':fontcolor=white@0.3:fontsize=50:x=(w-text_w)/2:y=h-250[v_out]"
    )
    subprocess.run(f"ffmpeg -y -i raw.mp4 -stream_loop -1 -i music.mp3 -filter_complex \"{f_complex}\" -map \"[v_out]\" -map 1:a -c:v libx264 -pix_fmt yuv420p -preset superfast -t 15 final_video.mp4", shell=True)
    print("--- CRYPTO READY ---")

if __name__ == "__main__":
    asyncio.run(main())
