import os
from PIL import Image, ImageDraw, ImageFont

def generate_screenshots():
    os.makedirs('screenshots', exist_ok=True)
    
    # 1. Desktop screenshot (1280 x 720)
    dw, dh = 1280, 720
    desktop = Image.new("RGBA", (dw, dh), (2, 6, 23, 255)) # slate-950
    draw = ImageDraw.Draw(desktop)
    
    # Header bar
    draw.rectangle([0, 0, dw, 64], fill=(15, 23, 42, 240)) # slate-900
    draw.line([0, 64, dw, 64], fill=(30, 41, 59, 255), width=1)
    
    # Header icon & title
    draw.rounded_rectangle([32, 14, 68, 50], radius=8, fill=(16, 185, 129, 255))
    draw.rectangle([80, 20, 360, 32], fill=(248, 250, 252, 255)) # title placeholder bar
    draw.rectangle([80, 38, 280, 46], fill=(148, 163, 184, 180)) # subtitle placeholder
    
    # Header buttons right
    draw.rounded_rectangle([dw - 420, 16, dw - 300, 48], radius=8, fill=(16, 185, 129, 255)) # Diapositivas
    draw.rounded_rectangle([dw - 290, 16, dw - 180, 48], radius=8, fill=(30, 41, 59, 255)) # Guía
    draw.rounded_rectangle([dw - 170, 16, dw - 50, 48], radius=8, fill=(245, 158, 11, 255)) # PPTX
    
    # Main slide card
    card_margin_x, card_margin_y = 60, 95
    card_w = dw - (card_margin_x * 2)
    card_h = dh - card_margin_y - 80
    draw.rounded_rectangle([card_margin_x, card_margin_y, card_margin_x + card_w, card_margin_y + card_h], radius=24, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    
    # Inside slide card: Badge
    draw.rounded_rectangle([card_margin_x + 40, card_margin_y + 40, card_margin_x + 280, card_margin_y + 68], radius=14, fill=(16, 185, 129, 30), outline=(16, 185, 129, 80), width=1)
    # Big title lines
    draw.rectangle([card_margin_x + 40, card_margin_y + 90, card_margin_x + 580, card_margin_y + 130], fill=(255, 255, 255, 255))
    draw.rectangle([card_margin_x + 40, card_margin_y + 140, card_margin_x + 520, card_margin_y + 175], fill=(52, 211, 153, 255))
    # Subtitle
    draw.rectangle([card_margin_x + 40, card_margin_y + 200, card_margin_x + 560, card_margin_y + 215], fill=(203, 213, 225, 200))
    draw.rectangle([card_margin_x + 40, card_margin_y + 225, card_margin_x + 480, card_margin_y + 240], fill=(203, 213, 225, 200))
    
    # 4 Grid Stat Cards on right
    grid_x = card_margin_x + 640
    for idx, (stat, col) in enumerate([("-50%", (16, 185, 129)), ("1,2x", (20, 184, 166)), ("Zona 2", (245, 158, 11)), ("BDNF", (168, 85, 247))]):
        gx = grid_x + (idx % 2) * 230
        gy = card_margin_y + 60 + (idx // 2) * 180
        draw.rounded_rectangle([gx, gy, gx + 210, gy + 155], radius=16, fill=(30, 41, 59, 200), outline=col + (90,), width=1)
        # stat accent bar
        draw.rectangle([gx + 20, gy + 30, gx + 90, gy + 65], fill=col + (255,))
        draw.rectangle([gx + 20, gy + 85, gx + 180, gy + 98], fill=(203, 213, 225, 220))
        draw.rectangle([gx + 20, gy + 108, gx + 150, gy + 120], fill=(148, 163, 184, 180))
        
    # Bottom navigation controls
    draw.rounded_rectangle([card_margin_x, dh - 60, card_margin_x + 120, dh - 20], radius=12, fill=(30, 41, 59, 255)) # Anterior
    draw.rounded_rectangle([card_margin_x + 140, dh - 60, card_margin_x + 500, dh - 20], radius=12, fill=(6, 78, 59, 120), outline=(16, 185, 129, 60), width=1) # Note
    draw.rounded_rectangle([dw - card_margin_x - 130, dh - 60, dw - card_margin_x, dh - 20], radius=12, fill=(16, 185, 129, 255)) # Siguiente
    
    desktop.save('screenshots/desktop.png', 'PNG')
    print("screenshots/desktop.png created")
    
    # 2. Mobile screenshot (750 x 1334 - iPhone 8 / SE standard PWA portrait ratio)
    mw, mh = 750, 1334
    mobile = Image.new("RGBA", (mw, mh), (2, 6, 23, 255))
    mdraw = ImageDraw.Draw(mobile)
    
    # Top safe area / status bar placeholder
    mdraw.rectangle([0, 0, mw, 88], fill=(15, 23, 42, 240))
    # Header
    mdraw.rounded_rectangle([30, 24, 72, 66], radius=10, fill=(16, 185, 129, 255))
    mdraw.rectangle([88, 30, 420, 46], fill=(248, 250, 252, 255))
    mdraw.rectangle([88, 52, 300, 62], fill=(148, 163, 184, 180))
    
    # Mode switch buttons
    mdraw.rounded_rectangle([mw - 240, 28, mw - 130, 62], radius=8, fill=(16, 185, 129, 255))
    mdraw.rounded_rectangle([mw - 120, 28, mw - 25, 62], radius=8, fill=(30, 41, 59, 255))
    
    # Progress bar
    mdraw.rectangle([30, 110, mw - 30, 118], fill=(30, 41, 59, 255))
    mdraw.rectangle([30, 110, 120, 118], fill=(16, 185, 129, 255))
    
    # Slide cards
    sc_y = 150
    mdraw.rounded_rectangle([30, sc_y, mw - 30, mh - 130], radius=24, fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    
    # Title
    mdraw.rounded_rectangle([60, sc_y + 40, 360, sc_y + 70], radius=12, fill=(16, 185, 129, 30), outline=(16, 185, 129, 80), width=1)
    mdraw.rectangle([60, sc_y + 90, mw - 60, sc_y + 130], fill=(255, 255, 255, 255))
    mdraw.rectangle([60, sc_y + 140, mw - 120, sc_y + 180], fill=(52, 211, 153, 255))
    mdraw.rectangle([60, sc_y + 205, mw - 80, sc_y + 225], fill=(203, 213, 225, 200))
    mdraw.rectangle([60, sc_y + 235, mw - 140, sc_y + 255], fill=(203, 213, 225, 200))
    
    # 4 Stat cards stacked 2x2
    for idx, (stat, col) in enumerate([("-50%", (16, 185, 129)), ("1,2x", (20, 184, 166)), ("Zona 2", (245, 158, 11)), ("BDNF", (168, 85, 247))]):
        gx = 60 + (idx % 2) * 320
        gy = sc_y + 320 + (idx // 2) * 220
        mdraw.rounded_rectangle([gx, gy, gx + 300, gy + 195], radius=16, fill=(30, 41, 59, 200), outline=col + (90,), width=1)
        mdraw.rectangle([gx + 25, gy + 30, gx + 120, gy + 75], fill=col + (255,))
        mdraw.rectangle([gx + 25, gy + 100, gx + 260, gy + 115], fill=(203, 213, 225, 220))
        mdraw.rectangle([gx + 25, gy + 128, gx + 210, gy + 142], fill=(148, 163, 184, 180))
        
    # Bottom action bar with safe area for iPhone
    mdraw.rounded_rectangle([30, mh - 110, 200, mh - 45], radius=14, fill=(30, 41, 59, 255))
    mdraw.rounded_rectangle([mw - 210, mh - 110, mw - 30, mh - 45], radius=14, fill=(16, 185, 129, 255))
    
    mobile.save('screenshots/mobile.png', 'PNG')
    print("screenshots/mobile.png created")

if __name__ == '__main__':
    generate_screenshots()
