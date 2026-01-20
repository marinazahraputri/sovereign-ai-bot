import asyncio, os, random, requests, subprocess, pickle, time, sys, textwrap, shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

GEMINI_API_KEY = 'AIzaSyBPazkoqLmIjEzcoO1Etnozycq3sroZVH4'
PEXELS_API_KEY = '845Gyp45DUDD9JD8CY7mQyfUaVpG8C73nZED3M0d82thoA0hNR4VzjBQ'
FREESOUND_API_KEY = 'RHcVaJy0EhVmOjJWTUAriLfppojg4WmvyIxkiihE'
WATERMARK = "TOBEHUMAN1%"

async def main():
    print("=== ASMR ENGINE: TOBEHUMAN1% ===")
    v_res = requests.get(f"https://api.pexels.com/videos/search?query=nature 4k&per_page=10&orientation=portrait", headers={"Authorization": PEXELS_API_KEY}).json()
    v_url = random.choice(v_res['videos'])['video_files'][0]['link']
    with open("raw.mp4", 'wb') as f: f.write(requests.get(v_url).content)
    
    os.system(f"wget -O asmr.mp3 https://www.soundjay.com/nature/river-1.mp3")
    
    f_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        "unsharp=5:5:1.5,eq=contrast=1.3:saturation=1.5[fin];"
        f"[fin]drawtext=text='{WATERMARK}':fontcolor=white@0.4:fontsize=50:x=(w-text_w)/2:y=h-200"
    )
    subprocess.run(f"ffmpeg -y -i raw.mp4 -stream_loop -1 -i asmr.mp3 -filter_complex \"{f_complex}\" -map 0:v -map 1:a -c:v libx264 -pix_fmt yuv420p -preset superfast -t 15 final_video.mp4", shell=True)
    print("--- ASMR READY ---")

if __name__ == "__main__":
    asyncio.run(main())
