#!/usr/bin/env python3
import sys, os, io
import numpy as np
from PIL import Image, ImageEnhance

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from rembg import remove as rembg_remove
except ImportError:
    rembg_remove = None

def remove_background(image: Image.Image) -> Image.Image:
    if rembg_remove is not None:
        print("[*] Removing background with U2Net (rembg)...")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        output_bytes = rembg_remove(img_byte_arr.getvalue())
        return Image.open(io.BytesIO(output_bytes)).convert("RGBA")
    print("[!] rembg not available, continuing with standard channels...")
    return image.convert("RGBA")

def autocrop_alpha(image: Image.Image, padding: int = 15) -> Image.Image:
    alpha = image.split()[-1]
    bbox = alpha.getbbox()
    if bbox:
        left, upper, right, lower = bbox
        width, height = image.size
        left = max(0, left - padding)
        upper = max(0, upper - padding)
        right = min(width, right + padding)
        lower = min(height, lower + padding)
        return image.crop((left, upper, right, lower))
    return image

def apply_clahe(gray_np: np.ndarray) -> np.ndarray:
    if cv2 is not None:
        clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8, 8))
        return clahe.apply(gray_np)
    min_v, max_v = float(gray_np.min()), float(gray_np.max())
    if max_v > min_v:
        return ((gray_np.astype(float) - min_v) / (max_v - min_v) * 255.0).astype(np.uint8)
    return gray_np

def process_portrait(input_path: str, output_path: str = "source-prepped.png", target_width: int = 400):
    if not os.path.exists(input_path):
        print(f"[!] Error: {input_path} not found")
        sys.exit(1)
    print(f"[*] Loading: {input_path}")
    raw = Image.open(input_path)
    nobg = remove_background(raw)
    cropped = autocrop_alpha(nobg, padding=15)
    bg = Image.new("RGBA", cropped.size, (0, 0, 0, 255))
    composite = Image.alpha_composite(bg, cropped).convert("RGB")
    aspect = composite.size[1] / composite.size[0]
    target_height = int(target_width * aspect)
    resized = composite.resize((target_width, target_height), Image.Resampling.LANCZOS)
    np_img = np.array(resized.convert("L"))
    enhanced_np = apply_clahe(np_img)
    enhanced = Image.fromarray(enhanced_np)
    final_img = ImageEnhance.Sharpness(enhanced).enhance(1.4)
    final_img.save(output_path, "PNG")
    print(f"[+] Successfully generated prepped photo: {output_path} ({final_img.size[0]}x{final_img.size[1]})")

if __name__ == "__main__":
    in_f = sys.argv[1] if len(sys.argv) > 1 else "hero.png"
    out_f = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    process_portrait(in_f, out_f)
