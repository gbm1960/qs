import os
import math
from PIL import Image, ImageDraw, ImageFilter

def draw_footprint_shapes(draw, center_x, center_y, scale, angle_deg, is_left, color_tuple):
    """
    Renders an anatomical yet modern minimalist footprint using vector math
    """
    canvas_w, canvas_h = int(500 * scale), int(750 * scale)
    fp = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(fp)
    
    # Scale coordinates
    s = scale
    cx = canvas_w / 2
    
    # Heel (calcaño): rounded shape at bottom
    heel_cy = canvas_h * 0.76
    heel_rx = 52 * s
    heel_ry = 68 * s
    d.ellipse([cx - heel_rx, heel_cy - heel_ry, cx + heel_rx, heel_cy + heel_ry], fill=color_tuple)
    
    # Sole / Metatarsal ball: broader shape at top
    sole_cy = canvas_h * 0.44
    sole_rx = 74 * s
    sole_ry = 98 * s
    d.ellipse([cx - sole_rx, sole_cy - sole_ry, cx + sole_rx, sole_cy + sole_ry], fill=color_tuple)
    
    # Connecting arch (curved toward the outside for lateral border)
    # Left foot has arch on right (inner side), lateral border on left (outer side)
    outer_x = cx - 58 * s if is_left else cx + 58 * s
    inner_x = cx + 22 * s if is_left else cx - 22 * s
    
    bridge = [
        (cx - 48 * s, heel_cy - 20 * s),
        (cx + 48 * s, heel_cy - 20 * s),
        (cx + 62 * s, sole_cy + 30 * s),
        (cx - 62 * s, sole_cy + 30 * s)
    ]
    d.polygon(bridge, fill=color_tuple)
    
    # If left foot, cut out / smooth the inner medial arch
    # Toes (5 in an aerodynamic upward arch)
    # Big toe is largest and positioned on the medial (inner) side
    toes = [
        # (rel_x, rel_y, radius)
        (38 * s if is_left else -38 * s, canvas_h * 0.22, 22 * s), # Big toe
        (10 * s if is_left else -10 * s, canvas_h * 0.20, 16 * s), # 2nd toe
        (-14 * s if is_left else 14 * s, canvas_h * 0.22, 14 * s), # 3rd toe
        (-34 * s if is_left else 34 * s, canvas_h * 0.26, 12 * s), # 4th toe
        (-50 * s if is_left else 50 * s, canvas_h * 0.32, 10 * s), # 5th toe
    ]
    
    for tx, ty, r in toes:
        d.ellipse([cx + tx - r, ty - r, cx + tx + r, ty + r], fill=color_tuple)
        
    # Rotate
    rotated = fp.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    return rotated

def generate_icon(size=512, maskable=False, is_ios=False):
    # Base supersampling 2x for ultra smooth curves
    ss = 2
    w = size * ss
    h = size * ss
    
    # Background slate-950
    bg_color = (2, 6, 23, 255) # #020617
    img = Image.new("RGBA", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    cx, cy = w // 2, h // 2
    
    # Glow layer
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    glow_radius = int(w * 0.42)
    for r in range(glow_radius, 0, -6 * ss):
        t = r / glow_radius
        alpha = int(45 * (1.0 - t))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 185, 129, alpha))
        
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)
    
    # Modern concentric orbital lines representing vitality / steps
    for ring_r in [int(w * 0.36), int(w * 0.42)]:
        draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], outline=(52, 211, 153, 35), width=max(2, 2 * ss))
        
    # Content scaling: Android maskable icons need safety zone in inner 80% (0.4 radius)
    scale_factor = (0.72 if maskable else 0.88) * (size / 512.0) * ss
    
    # Dynamic duo of footsteps walking forward
    # Footprint 1: Left foot, trailing slightly, emerald-400
    color_trail = (52, 211, 153, 220) # #34d399
    fp_left = draw_footprint_shapes(draw, cx, cy, scale=0.72 * scale_factor, angle_deg=-14, is_left=True, color_tuple=color_trail)
    
    # Footprint 2: Right foot, leading forward, vibrant teal/emerald glow
    color_lead = (16, 185, 129, 255) # #10b981
    fp_right = draw_footprint_shapes(draw, cx, cy, scale=0.78 * scale_factor, angle_deg=14, is_left=False, color_tuple=color_lead)
    
    # Placement
    left_x = int(cx - fp_left.width * 0.88)
    left_y = int(cy - fp_left.height * 0.15)
    
    right_x = int(cx - fp_right.width * 0.15)
    right_y = int(cy - fp_right.height * 0.80)
    
    img.paste(fp_left, (left_x, left_y), fp_left)
    img.paste(fp_right, (right_x, right_y), fp_right)
    
    draw = ImageDraw.Draw(img)
    # Subtle sparkling star / energy spark at the top right
    spark_cx = int(cx + w * 0.32)
    spark_cy = int(cy - h * 0.30)
    spark_r = int(12 * ss * (size / 512.0))
    draw.ellipse([spark_cx - spark_r, spark_cy - spark_r, spark_cx + spark_r, spark_cy + spark_r], fill=(245, 158, 11, 255)) # amber-500
    
    # If not maskable, we give a subtle rounded card outline for standard desktop app
    if not maskable and not is_ios:
        pad = int(14 * ss * (size / 512.0))
        border_r = int(110 * ss * (size / 512.0))
        draw.rounded_rectangle([pad, pad, w - pad, h - pad], radius=border_r, outline=(52, 211, 153, 60), width=max(2, 3 * ss))
    
    # Downsample back to target size with highest quality LANCZOS
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

def create_svg():
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="leadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#10b981" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="512" height="512" rx="115" fill="url(#bgGrad)"/>
  <rect width="500" height="500" x="6" y="6" rx="110" fill="none" stroke="#34d399" stroke-width="2" stroke-opacity="0.25"/>

  <!-- Radial Glow -->
  <circle cx="256" cy="256" r="210" fill="url(#glowGrad)"/>
  <circle cx="256" cy="256" r="195" fill="none" stroke="#34d399" stroke-width="1.5" stroke-opacity="0.2" stroke-dasharray="6 8"/>

  <!-- Left Footprint (Trailing) -->
  <g transform="translate(140, 240) rotate(-14) scale(0.65)" fill="#34d399" opacity="0.85">
    <ellipse cx="60" cy="190" rx="36" ry="46" />
    <path d="M 30,120 C 25,160 30,175 32,190 C 70,190 85,180 88,160 C 92,140 90,115 88,100 Z" />
    <ellipse cx="60" cy="95" rx="50" ry="60" />
    <ellipse cx="90" cy="18" rx="15" ry="18" />
    <ellipse cx="68" cy="14" rx="11" ry="14" />
    <ellipse cx="48" cy="18" rx="9" ry="12" />
    <ellipse cx="30" cy="26" rx="8" ry="10" />
    <ellipse cx="14" cy="38" rx="6" ry="8" />
  </g>

  <!-- Right Footprint (Leading) -->
  <g transform="translate(270, 110) rotate(14) scale(0.72)" fill="url(#leadGrad)" filter="url(#shadow)">
    <ellipse cx="60" cy="190" rx="36" ry="46" />
    <path d="M 30,100 C 28,115 26,140 30,160 C 33,180 48,190 86,190 C 88,175 93,160 88,120 Z" />
    <ellipse cx="60" cy="95" rx="50" ry="60" />
    <ellipse cx="30" cy="18" rx="15" ry="18" />
    <ellipse cx="52" cy="14" rx="11" ry="14" />
    <ellipse cx="72" cy="18" rx="9" ry="12" />
    <ellipse cx="90" cy="26" rx="8" ry="10" />
    <ellipse cx="106" cy="38" rx="6" ry="8" />
  </g>

  <!-- Vitality Star Accent -->
  <circle cx="410" cy="100" r="10" fill="#f59e0b" filter="url(#shadow)"/>
  <circle cx="410" cy="100" r="16" fill="none" stroke="#f59e0b" stroke-width="2" stroke-opacity="0.4"/>
</svg>'''
    with open('icons/favicon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("icons/favicon.svg created")

def main():
    os.makedirs('icons', exist_ok=True)
    
    print("Generating SVG favicon...")
    create_svg()
    
    targets = [
        ("icons/icon-512x512.png", 512, False, False),
        ("icons/icon-192x192.png", 192, False, False),
        ("icons/icon-maskable-512x512.png", 512, True, False),
        ("icons/icon-maskable-192x192.png", 192, True, False),
        ("icons/apple-touch-icon-180x180.png", 180, False, True),
        ("icons/apple-touch-icon.png", 180, False, True),
        ("icons/favicon-32x32.png", 32, False, False),
        ("icons/favicon-16x16.png", 16, False, False),
    ]
    
    for filename, size, maskable, is_ios in targets:
        print(f"Generating {filename} ({size}x{size}, maskable={maskable})...")
        img = generate_icon(size=size, maskable=maskable, is_ios=is_ios)
        img.save(filename, "PNG", optimize=True)
        
    print("All icons successfully generated!")

if __name__ == '__main__':
    main()
