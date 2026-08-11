#!/usr/bin/env python3
"""
SpectreBand Logo Generator
Generates aesthetic SVG logos with random variations based on seed.
Usage: python generate_logo.py [seed]
"""

import hashlib, random, sys, os

def generate_logo(seed=None, output_dir="assets"):
    if seed is None:
        seed = hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]

    random.seed(seed)

    # Color palettes - cyberpunk/paintball aesthetic
    palettes = [
        ["#0f0f23", "#6366f1", "#a78bfa", "#f472b6", "#10b981"],  # Indigo/pink/green
        ["#0a0a0a", "#ef4444", "#f59e0b", "#10b981", "#3b82f6"],   # Red/amber/green/blue
        ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#533483"],   # Deep blue/red
        ["#0d1117", "#58a6ff", "#238636", "#8957e5", "#f0883e"],   # GitHub dark
    ]
    palette = random.choice(palettes)
    bg, primary, secondary, accent, highlight = palette

    # Random geometric parameters
    cx, cy = 200, 200
    r_base = random.randint(60, 80)
    num_rings = random.randint(3, 5)
    num_dots = random.randint(8, 16)
    rotation = random.randint(0, 360)

    # Generate concentric radar rings
    rings = []
    for i in range(num_rings):
        r = r_base + i * 25
        opacity = 0.3 + (i / num_rings) * 0.5
        dash = random.choice(["", f'stroke-dasharray="{random.randint(3,8)} {random.randint(3,8)}"'])
        rings.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{primary}" stroke-width="{2-i*0.3:.1f}" opacity="{opacity:.2f}" {dash}/>')

    # Generate sweep line (radar sweep)
    sweep_angle = random.randint(0, 360)
    sweep_x = cx + (r_base + num_rings * 25) * 0.9 * 0.707
    sweep_y = cy - (r_base + num_rings * 25) * 0.9 * 0.707

    # Generate player dots
    dots = []
    for i in range(num_dots):
        angle = (360 / num_dots) * i + random.randint(-15, 15)
        dist = random.randint(r_base - 20, r_base + num_rings * 25 - 10)
        dx = cx + dist * 0.01745 * angle  # rough approx
        # Use proper trig
        import math
        rad = math.radians(angle)
        dx = cx + dist * math.cos(rad)
        dy = cy + dist * math.sin(rad)
        color = random.choice([secondary, accent, highlight])
        size = random.choice([3, 4, 5])
        glow = random.choice(["", f'<circle cx="{dx}" cy="{dy}" r="{size+4}" fill="{color}" opacity="0.3"/>'])
        dots.append(f'{glow}<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{size}" fill="{color}"/>')

    # Generate particle trails (random effect 1)
    trails = []
    for i in range(random.randint(5, 12)):
        angle = random.randint(0, 360)
        dist = random.randint(r_base + 20, r_base + num_rings * 25)
        import math
        rad = math.radians(angle)
        x1 = cx + (dist - 15) * math.cos(rad)
        y1 = cy + (dist - 15) * math.sin(rad)
        x2 = cx + (dist + 15) * math.cos(rad)
        y2 = cy + (dist + 15) * math.sin(rad)
        trails.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{accent}" stroke-width="1" opacity="0.4"/>')

    # Generate hex grid overlay (random effect 2)
    hexes = []
    if random.random() > 0.5:
        hex_size = random.randint(15, 25)
        for row in range(-5, 6):
            for col in range(-5, 6):
                import math
                hx = cx + col * hex_size * 1.5
                hy = cy + row * hex_size * math.sqrt(3) + (col % 2) * hex_size * math.sqrt(3) / 2
                if (hx - cx)**2 + (hy - cy)**2 < (r_base + num_rings * 25 + 20)**2:
                    hexes.append(f'<polygon points="{hx-hex_size/2},{hy-hex_size*0.289} {hx+hex_size/2},{hy-hex_size*0.289} {hx+hex_size},{hy} {hx+hex_size/2},{hy+hex_size*0.289} {hx-hex_size/2},{hy+hex_size*0.289} {hx-hex_size},{hy}" fill="none" stroke="{secondary}" stroke-width="0.5" opacity="0.15"/>')

    # Generate glow pulses (random effect 3)
    pulses = []
    for i in range(random.randint(2, 4)):
        pr = random.randint(r_base - 10, r_base + num_rings * 25 - 20)
        pulses.append(f'<circle cx="{cx}" cy="{cy}" r="{pr}" fill="none" stroke="{highlight}" stroke-width="1" opacity="0.2"><animate attributeName="r" values="{pr};{pr+10};{pr}" dur="{2+random.random()*2:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.2;0.05;0.2" dur="{2+random.random()*2:.1f}s" repeatCount="indefinite"/></circle>')

    # Assemble SVG
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{bg}" stop-opacity="1"/>
      <stop offset="100%" stop-color="{palette[1]}" stop-opacity="0.3"/>
    </radialGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="strong-glow">
      <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="400" height="400" fill="url(#bg)"/>

  <!-- Hex grid overlay -->
  {chr(10).join(hexes)}

  <!-- Radar rings -->
  {chr(10).join(rings)}

  <!-- Center crosshair -->
  <line x1="{cx-10}" y1="{cy}" x2="{cx+10}" y2="{cy}" stroke="{primary}" stroke-width="2"/>
  <line x1="{cx}" y1="{cy-10}" x2="{cx}" y2="{cy+10}" stroke="{primary}" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="4" fill="{highlight}" filter="url(#glow)"/>

  <!-- Sweep line -->
  <line x1="{cx}" y1="{cy}" x2="{sweep_x:.1f}" y2="{sweep_y:.1f}" stroke="{accent}" stroke-width="2" opacity="0.6" filter="url(#glow)">
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/>
  </line>

  <!-- Particle trails -->
  {chr(10).join(trails)}

  <!-- Player dots -->
  {chr(10).join(dots)}

  <!-- Glow pulses -->
  {chr(10).join(pulses)}

  <!-- Text -->
  <text x="200" y="360" text-anchor="middle" font-family="'Segoe UI', 'Helvetica Neue', sans-serif" font-size="28" font-weight="bold" fill="{primary}" letter-spacing="4" filter="url(#glow)">SPECTRE</text>
  <text x="200" y="385" text-anchor="middle" font-family="'Segoe UI', 'Helvetica Neue', sans-serif" font-size="14" font-weight="300" fill="{secondary}" letter-spacing="8">BAND</text>

  <!-- Seed watermark -->
  <text x="390" y="390" text-anchor="end" font-family="monospace" font-size="8" fill="{secondary}" opacity="0.3">{seed[:8]}</text>
</svg>"""

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/logo_{seed[:8]}.svg"
    with open(filename, "w") as f:
        f.write(svg)

    print(f"Generated: {filename} (seed: {seed})")
    return filename, seed

if __name__ == "__main__":
    seed = sys.argv[1] if len(sys.argv) > 1 else None

    # Generate base logo
    f1, s1 = generate_logo(seed, "assets")

    # Generate 3 random variations
    for i in range(3):
        variant_seed = hashlib.sha256(f"{s1}_variant_{i}".encode()).hexdigest()[:16]
        generate_logo(variant_seed, "assets")

    print("\nDone! Check assets/ for generated logos.")
