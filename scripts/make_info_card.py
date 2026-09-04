#!/usr/bin/env python3
import sys, os, html

def generate_info_card(output_path: str = "info-card.svg", width: int = 490, height: int = 490):
    entries = [
        ("USER", "rahad", "#00f2fe"),
        ("HOST", "Rahad Hasan (@rahadalways)", "#e6edf3"),
        ("ROLE", "Full Stack Engineer", "#f59e0b"),
        ("LOCATION", "Dhaka, Bangladesh [UTC+6]", "#e6edf3"),
        ("UPTIME", "Building & Shipping 24/7", "#10b981"),
        ("FRONTEND", "React + TypeScript + Next.js + Tailwind + Three.js", "#38bdf8"),
        ("BACKEND", "Node.js + Express + Python + MySQL + Supabase", "#818cf8"),
        ("MOBILE", "React Native + Flutter", "#ec4899"),
        ("TOOLS", "Git + GitHub Actions + Docker + Postman + Vercel", "#a7f3d0"),
        ("PORTFOLIO", "https://rahadhasan.com", "#fbbf24"),
        ("EMAIL", "rahad@rahadhasan.com", "#e6edf3"),
        ("STATUS", "+ Open to High-Impact Opportunities", "#34d399"),
    ]

    css_rules = []
    svg_rows = []
    start_y = 66
    line_spacing = 25.5

    for idx, (key, val, val_color) in enumerate(entries):
        delay = 0.1 + (idx * 0.05)
        css_rules.append(f".row-{idx} {{ animation: rowIn 0.45s ease-out {delay:.3f}s forwards; opacity: 0; }}")
        y = start_y + (idx * line_spacing)

        svg_rows.append(f'''    <g class="row-{idx}">
      <text class="key" x="22" y="{y:.1f}">{html.escape(key)}</text>
      <text class="separator" x="115" y="{y:.1f}">+</text>
      <text class="val" fill="{val_color}" x="135" y="{y:.1f}">{html.escape(val)}</text>
    </g>''')

    css_block = "\n      ".join(css_rules)
    rows_block = "\n".join(svg_rows)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="infoCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e0e11" />
      <stop offset="50%" stop-color="#0a0a0c" />
      <stop offset="100%" stop-color="#050507" />
    </linearGradient>

    <linearGradient id="infoBorderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37" stop-opacity="0.5" />
      <stop offset="30%" stop-color="#2a2a2e" stop-opacity="0.8" />
      <stop offset="70%" stop-color="#1b1b1f" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0.3" />
    </linearGradient>

    <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D4AF37" />
      <stop offset="50%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#00f2fe" />
    </linearGradient>
  </defs>

  <style>
    @keyframes rowIn {{
      from {{ opacity: 0; transform: translateX(-4px); }}
      to {{ opacity: 1; transform: translateX(0); }}
    }}
    .term-title {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 600;
      fill: #8b949e;
      letter-spacing: 0.5px;
    }}
    .key {{
      font-family: 'JetBrains Mono', 'Fira Code', monospace;
      font-size: 11px;
      font-weight: 700;
      fill: #D4AF37;
      letter-spacing: 0.5px;
    }}
    .separator {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 600;
      fill: #4b5563;
    }}
    .val {{
      font-family: 'JetBrains Mono', 'Segoe UI', monospace;
      font-size: 10.8px;
      font-weight: 500;
      letter-spacing: 0.3px;
    }}
    .term-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 9.5px;
      font-weight: 600;
      fill: #10b981;
    }}
    .palette-box {{
      rx: 2;
      ry: 2;
    }}
    {css_block}
  </style>

  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="url(#infoCardBg)" stroke="url(#infoBorderGrad)" stroke-width="1.5" />
  <path d="M 1 15 C 1 7.268 7.268 1 15 1 L {width - 15} 1 C {width - 7.268} 1 {width - 1} 7.268 {width - 1} 15 L {width - 1} 38 L 1 38 Z" fill="#141419" />
  <line x1="1" y1="38" x2="{width - 1}" y2="38" stroke="#222228" stroke-width="1" />

  <circle cx="20" cy="19" r="5.5" fill="#ff5f56" stroke="#e0443e" stroke-width="0.5" />
  <circle cx="36" cy="19" r="5.5" fill="#ffbd2e" stroke="#dea123" stroke-width="0.5" />
  <circle cx="52" cy="19" r="5.5" fill="#27c93f" stroke="#1aab29" stroke-width="0.5" />

  <text class="term-title" x="{width / 2}" y="23" text-anchor="middle">The Cipher Stack // System Info</text>
  <text class="term-badge" x="{width - 18}" y="23" text-anchor="end">+ ONLINE</text>

  <g>
{rows_block}
  </g>

  <line x1="1" y1="{height - 52}" x2="{width - 1}" y2="{height - 52}" stroke="#1f1f26" stroke-width="1" />
  <text class="key" x="22" y="{height - 34}">SYSTEM_LOAD</text>
  <rect x="115" y="{height - 43}" width="160" height="11" rx="4" fill="#1a1a22" stroke="#2a2a35" stroke-width="0.8" />
  <rect x="116" y="{height - 42}" width="138" height="9" rx="3" fill="url(#barGradient)" />
  <text class="val" fill="#10b981" x="284" y="{height - 34}">88% OPTIMIZED</text>

  <g transform="translate({width - 135}, {height - 43})">
    <rect class="palette-box" x="0" y="0" width="12" height="11" fill="#ff5f56" />
    <rect class="palette-box" x="15" y="0" width="12" height="11" fill="#ffbd2e" />
    <rect class="palette-box" x="30" y="0" width="12" height="11" fill="#27c93f" />
    <rect class="palette-box" x="45" y="0" width="12" height="11" fill="#00f2fe" />
    <rect class="palette-box" x="60" y="0" width="12" height="11" fill="#818cf8" />
    <rect class="palette-box" x="75" y="0" width="12" height="11" fill="#ec4899" />
    <rect class="palette-box" x="90" y="0" width="12" height="11" fill="#D4AF37" />
    <rect class="palette-box" x="105" y="0" width="12" height="11" fill="#e6edf3" />
  </g>

  <text class="val" fill="#6e7681" x="22" y="{height - 12}">CIPHER_ENV: v3.4.0-release</text>
  <text class="val" fill="#6e7681" x="{width - 22}" y="{height - 12}" text-anchor="end">KERNEL: LINUX_x86_64</text>
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated Info Card SVG: {output_path} ({width}x{height})")

if __name__ == "__main__":
    out_svg = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
    generate_info_card(out_svg, width=490, height=490)
