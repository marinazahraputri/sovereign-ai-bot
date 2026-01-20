from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail():
    # Ukuran Shorts/Reels (1080x1920)
    width, height = 1080, 1920
    
    # Membuat background Hitam Pekat (Deep Black)
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Menggunakan font yang sudah ada di folder
    font_path = "font.ttf"
    if not os.path.exists(font_path):
        print("Font tidak ditemukan, mendownload...")
        os.system("wget -O font.ttf 'https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf'")
    
    # Ukuran Font
    font_large = ImageFont.truetype(font_path, 130)
    font_huge = ImageFont.truetype(font_path, 160)
    
    # Baris 1: EDITING MANUAL (Putih)
    draw.text((width/2, 500), "EDITING", fill=(255, 255, 255), font=font_large, anchor="mm")
    draw.text((width/2, 650), "MANUAL", fill=(255, 255, 255), font=font_large, anchor="mm")
    
    # Baris 2: IS DEAD (Merah Agresif)
    # Menambahkan garis coretan (Strike-through)
    draw.text((width/2, 900), "IS DEAD", fill=(255, 0, 0), font=font_huge, anchor="mm")
    draw.line((250, 900, 830, 900), fill=(255, 0, 0), width=20)
    
    # Baris 3: 100% AUTO BY AI (Hijau Neon)
    draw.rectangle([100, 1150, 980, 1450], outline=(0, 255, 0), width=10) # Kotak Bingkai
    draw.text((width/2, 1300), "100% AUTO\nBY AI", fill=(0, 255, 0), font=font_large, anchor="mm", align="center")
    
    # Watermark
    draw.text((width/2, 1800), "@pcahtalua8776", fill=(100, 100, 100), font=ImageFont.truetype(font_path, 40), anchor="mm")

    # Simpan sebagai JPG kualitas maksimal
    img.save("thumbnail_final.jpg", "JPEG", quality=100)
    print("--- 100% SUCCESS: Thumbnail Berhasil Dibuat (thumbnail_final.jpg) ---")

if __name__ == "__main__":
    create_thumbnail()
