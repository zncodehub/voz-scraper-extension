"""
make_icons.py — Tạo icon PNG placeholder cho extension.
Chạy 1 lần: python make_icons.py
Yêu cầu: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    for size in [16, 48, 128]:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background đỏ VOZ
        draw.rounded_rectangle([0, 0, size-1, size-1],
                                radius=size//5,
                                fill=(232, 57, 60, 255))
        
        # Chữ V
        font_size = int(size * 0.55)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text = "V"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (size - tw) // 2 - bbox[0]
        y = (size - th) // 2 - bbox[1]
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        fname = f"icon{size}.png"
        img.save(fname)
        print(f"[+] {fname} created")

    print("✅ Icons created!")

except ImportError:
    print("Pillow không được cài. Chạy: pip install Pillow")
    print("Hoặc dùng bất kỳ icon 16x16 và 48x48 PNG nào, đặt tên icon16.png và icon48.png")
