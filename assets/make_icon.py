# assets/make_icon.py — generates assets/icon.icns (macOS) and assets/icon.ico (all platforms)
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent


def base(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.22)
    # rounded background gradient (approx: two stacked rounded rects)
    d.rounded_rectangle([0, 0, size, size], radius=r, fill=(15, 20, 25, 255))
    d.rounded_rectangle([0, 0, size, int(size * 0.6)], radius=r, fill=(27, 36, 48, 255))
    # green play triangle
    cx, cy, t = size * 0.5, size * 0.5, size * 0.16
    d.polygon([(cx - t, cy - t), (cx - t, cy + t), (cx + t * 1.2, cy)], fill=(61, 220, 132, 255))
    return img


def main():
    iconset = HERE / "icon.iconset"
    iconset.mkdir(exist_ok=True)
    for s in (16, 32, 64, 128, 256, 512, 1024):
        base(s).save(iconset / f"icon_{s}x{s}.png")
        base(s).save(iconset / f"icon_{s//2}x{s//2}@2x.png")
    if sys.platform == "darwin":
        subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(HERE / "icon.icns")], check=True)
        print("wrote", HERE / "icon.icns")

    # Windows .ico from the 256px render
    base(256).save(HERE / "icon.ico", format="ICO",
                   sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("wrote", HERE / "icon.ico")


if __name__ == "__main__":
    main()
