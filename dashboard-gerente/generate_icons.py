import os
from PIL import Image, ImageDraw


def draw_dashboard_symbol(img_size, maskable=False):
    """Generates a clean executive dashboard icon (grid + ascending bars + pulse node) with Slate+Emerald palette."""
    ss = 2
    w = img_size * ss
    h = img_size * ss

    bg_color = (2, 6, 23, 255)  # #020617 slate-950
    img = Image.new("RGBA", (w, h), bg_color)

    # Radial emerald glow
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = w // 2, h // 2
    glow_radius = int(w * 0.44)
    for r in range(glow_radius, 0, -6 * ss):
        t = r / glow_radius
        alpha = int(42 * (1.0 - t))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 185, 129, alpha))

    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Scale content for maskable safety zone (inner 72%) vs regular (88%)
    scale = (0.70 if maskable else 0.84)
    box_w = int(w * scale)
    box_h = int(h * scale)
    x0 = (w - box_w) // 2
    y0 = (h - box_h) // 2

    # Outer frame representing control panel
    frame_r = int(box_w * 0.22)
    draw.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h],
        radius=frame_r,
        fill=(15, 23, 42, 235),  # #0f172a slate-900
        outline=(16, 185, 129, 140),
        width=max(2, int(4 * ss * (img_size / 512.0)))
    )

    # Top header bar inside panel
    inner_pad = int(box_w * 0.14)
    dot_r = max(3, int(box_w * 0.025))
    dot_y = y0 + inner_pad
    draw.ellipse([x0 + inner_pad, dot_y, x0 + inner_pad + dot_r * 2, dot_y + dot_r * 2], fill=(45, 212, 191, 255))
    draw.ellipse([x0 + inner_pad + dot_r * 3, dot_y, x0 + inner_pad + dot_r * 5, dot_y + dot_r * 2], fill=(16, 185, 129, 200))

    # 3 ascending KPI bars
    bars_area_x0 = x0 + inner_pad
    bars_area_w = box_w - inner_pad * 2
    bars_bottom = y0 + box_h - inner_pad
    bar_w = int(bars_area_w * 0.24)
    gap = int((bars_area_w - bar_w * 3) / 2)

    heights = [0.32, 0.48, 0.64]
    colors = [
        (45, 212, 191, 200),   # teal-400
        (16, 185, 129, 235),   # emerald-500
        (52, 211, 153, 255),   # emerald-400
    ]

    for i, (hf, col) in enumerate(zip(heights, colors)):
        bx = bars_area_x0 + i * (bar_w + gap)
        bh = int(box_h * hf)
        by = bars_bottom - bh
        br = max(2, int(bar_w * 0.25))
        draw.rounded_rectangle([bx, by, bx + bar_w, bars_bottom], radius=br, fill=col)

    # Pulse / AI spark node above the highest bar
    node_cx = bars_area_x0 + 2 * (bar_w + gap) + bar_w // 2
    node_cy = y0 + int(box_h * 0.19)
    node_r = max(4, int(box_w * 0.042))
    draw.ellipse(
        [node_cx - node_r, node_cy - node_r, node_cx + node_r, node_cy + node_r],
        fill=(45, 212, 191, 255)
    )

    return img.resize((img_size, img_size), Image.Resampling.LANCZOS)


def create_svg(out_dir):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="115" fill="url(#bgGrad)"/>
  <rect x="44" y="44" width="424" height="424" rx="88" fill="#0f172a" stroke="#10b981" stroke-opacity="0.45" stroke-width="6"/>
  <circle cx="110" cy="112" r="12" fill="#2dd4bf"/>
  <circle cx="146" cy="112" r="12" fill="#10b981" fill-opacity="0.8"/>
  <rect x="96" y="272" width="84" height="140" rx="18" fill="#2dd4bf" fill-opacity="0.85"/>
  <rect x="214" y="208" width="84" height="204" rx="18" fill="#10b981" fill-opacity="0.92"/>
  <rect x="332" y="144" width="84" height="268" rx="18" fill="url(#barGrad)"/>
  <circle cx="374" cy="106" r="16" fill="#2dd4bf"/>
</svg>'''
    with open(os.path.join(out_dir, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    create_svg(icons_dir)

    targets = [
        ("icon-512x512.png", 512, False),
        ("icon-192x192.png", 192, False),
        ("icon-maskable-512x512.png", 512, True),
        ("icon-maskable-192x192.png", 192, True),
        ("apple-touch-icon-180x180.png", 180, False),
        ("apple-touch-icon.png", 180, False),
        ("favicon-32x32.png", 32, False),
        ("favicon-16x16.png", 16, False),
    ]

    for filename, size, maskable in targets:
        img = draw_dashboard_symbol(size, maskable=maskable)
        img.save(os.path.join(icons_dir, filename), "PNG", optimize=True)

    print("Generated all 9 icons in", icons_dir)


if __name__ == "__main__":
    main()
