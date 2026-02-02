import sys
import os
import cv2
import numpy as np
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    print("Error: PIL not found. pip install pillow")
    sys.exit(1)

def cv2_to_pil(cv_img):
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

def pil_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def beauty_face_algorithm(img):
    """
    模拟美颜相机的核心算法 (EPF + 肤色修正)
    """
    # 1. 边缘保持滤波 (Edge Preserving Filter)
    # 这是比双边滤波更先进的算法，常用于即时美颜
    # flags=1 (RECURS_FILTER) 速度快效果好
    # sigma_s: 空间域参数，越大越模糊 (磨皮力度)
    # sigma_r: 颜色域参数，越大越能把色差大的地方也磨平
    smoothed = cv2.edgePreservingFilter(img, flags=1, sigma_s=60, sigma_r=0.4)

    # 2. 细节混合 (High Pass Skin Smoothing)
    # 不直接用 smoothed，而是把它作为低频层，保留原图的一些纹理（如发丝），防止变成"塑料人"
    # 公式：Result = Src * k + Smoothed * (1-k)
    # k 越小磨皮越狠
    result = cv2.addWeighted(img, 0.3, smoothed, 0.7, 0)

    return result

def bloom_effect(img, intensity=0.4):
    """
    少女感柔光特效 (Orton Effect / Bloom)
    原理：将高斯模糊后的图与原图进行"滤色" (Screen) 混合
    这能有效掩盖噪点，让高光溢出，产生朦胧美。
    """
    # 1. 强高斯模糊
    blur = cv2.GaussianBlur(img, (0, 0), sigmaX=5, sigmaY=5)

    # 2. 混合 (Screen 模式模拟)
    # Screen公式: 1 - (1-a)*(1-b)
    # 但简单的 addWeighted (Linear Dodge) 在这里效果更好且不易过曝
    # 我们用加权平均模拟柔光：原图 + 模糊图 * 强度
    bloom = cv2.addWeighted(img, 1.0, blur, intensity, 0)

    return bloom

def color_grading(img):
    """
    日系少女感调色 (Color Grading)
    特点：青色阴影、粉色高光、低对比、高明度
    """
    # 转到 LAB 调整明度
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # 1. 提升整体亮度 (Brightness)
    l = cv2.add(l, 15)

    # 2. 降低对比度 (Fade effect)
    # 主要是提亮暗部
    l = l.astype(np.float32)
    l = (l - 128) * 0.9 + 128 + 10 # 0.9对比度，+10偏移
    l = np.clip(l, 0, 255).astype(np.uint8)

    lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # 3. 调整色温 (微调 BGR)
    # 增加一点蓝色(B)和红色(R)，减少绿色，营造粉嫩通透感
    b, g, r = cv2.split(img)
    b = cv2.add(b, 5) # 冷调背景
    r = cv2.add(r, 8) # 暖调皮肤/红宝石
    # g 保持不变或微减

    return cv2.merge((b, g, r))

def intelligent_sharpen(img):
    """
    智能锐化：只锐化纹理复杂的区域（珠宝），忽略平坦区域（背景/皮肤）
    """
    # 1. 计算梯度（边缘强度）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(sobelx, sobely)

    # 2. 生成锐化遮罩
    # 只有边缘强度 > 阈值的地方才锐化
    mask = magnitude > 30
    mask = mask.astype(np.float32)
    mask = cv2.GaussianBlur(mask, (5, 5), 0) # 柔化边缘

    # 3. USM 锐化整个图
    gaussian = cv2.GaussianBlur(img, (0, 0), 2.0)
    sharpened = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0)

    # 4. 混合
    # Result = Sharpened * Mask + Original * (1 - Mask)
    mask_3c = cv2.merge([mask, mask, mask])

    img_float = img.astype(np.float32)
    sharpened_float = sharpened.astype(np.float32)

    final = sharpened_float * mask_3c + img_float * (1.0 - mask_3c)
    return np.clip(final, 0, 255).astype(np.uint8)

def add_watermark_pil(pil_img, text="Tokyo Quilala"):
    draw = ImageDraw.Draw(pil_img)
    w, h = pil_img.size

    font_path = None
    possible_fonts = ["Didot.ttc", "GARA.TTF", "georgia.ttf", "times.ttf"]
    system_font_dir = "C:\\Windows\\Fonts"
    for f in possible_fonts:
        p = os.path.join(system_font_dir, f)
        if os.path.exists(p):
            font_path = p
            break

    font_size = int(w / 28) # 字体稍微再小一点，更精致
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    margin_x = int(w * 0.05)
    margin_y = int(h * 0.04)
    x = w - text_w - margin_x
    y = h - text_h - margin_y

    watermark_layer = Image.new('RGBA', pil_img.size, (0,0,0,0))
    draw_w = ImageDraw.Draw(watermark_layer)

    # 阴影更淡一点
    shadow_color = (0, 0, 0, 40)
    for off in range(1, 3):
        draw_w.text((x + off, y + off), text, font=font, fill=shadow_color)

    draw_w.text((x, y), text, font=font, fill=(255, 255, 255, 220))

    if pil_img.mode != 'RGBA':
        pil_img = pil_img.convert('RGBA')

    return Image.alpha_composite(pil_img, watermark_layer).convert('RGB')

def process_image(input_path, output_path, mode="jewelry"):
    print(f"Loading: {input_path}")
    img_cv = cv2.imdecode(np.fromfile(input_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img_cv is None:
        print(f"Failed to load: {input_path}")
        return

    # 1. 尺寸优化
    h, w = img_cv.shape[:2]
    target_w = 1600
    if w < target_w:
        scale = target_w / w
        new_h = int(h * scale)
        img_cv = cv2.resize(img_cv, (target_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    elif w > 3000:
        scale = 3000 / w
        new_h = int(h * scale)
        img_cv = cv2.resize(img_cv, (3000, new_h), interpolation=cv2.INTER_AREA)

    # 2. 全局强力降噪 (去除"斑点"的核心步骤)
    # fastNlMeansDenoisingColored 速度慢但效果最好，像美颜相机的"磨皮"档
    # h=5 (强度), hColor=10 (色彩去噪强度)
    print("   -> Denoising (Beauty Mode)...")
    img_cv = cv2.fastNlMeansDenoisingColored(img_cv, None, 5, 5, 7, 21)

    # 3. 边缘保持磨皮 (EPF)
    print("   -> Skin Smoothing...")
    img_cv = beauty_face_algorithm(img_cv)

    # 4. 日系调色 (Color Grading)
    print("   -> Color Grading...")
    img_cv = color_grading(img_cv)

    # 5. 智能锐化 (只锐化珠宝)
    # 因为前面磨皮了，这里要把珠宝的质感找回来
    print("   -> Smart Sharpening...")
    img_cv = intelligent_sharpen(img_cv)

    # 6. 柔光特效 (Bloom) - 少女感关键
    print("   -> Adding Bloom...")
    img_cv = bloom_effect(img_cv, intensity=0.25)

    # 7. 水印与保存
    img_pil = cv2_to_pil(img_cv)
    img_final = add_watermark_pil(img_pil, "Tokyo Quilala")
    img_final.save(output_path, quality=98, subsampling=0)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python image_enhancer.py <input> <output> [mode]")
        sys.exit(1)
    process_image(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "general")
