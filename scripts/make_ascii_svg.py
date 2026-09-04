#!/usr/bin/env python3
import sys, os, html
from PIL import Image

ASCII_RAMP = " .`:-=+*cs#%@"

def image_to_ascii_grid(image_path: str, cols: int = 56, rows: int = 40) -> list:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Cannot find image: {image_path}")
    img = Image.open(image_path).convert("L")
    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = img_resized.load()
    ramp_len = len(ASCII_RAMP)
    lines = []
    for r in range(rows):
        line_chars = []
        for c in range(cols):
            val = pixels[c, r]
            idx = int((val / 255.0) * (ramp_len - 1))
            line_chars.append(ASCII_RAMP[idx])
        lines.append("".join(line_chars))
    return lines

def generate_ascii_svg(lines: list, output_path: str = "hxni-ascii.svg", width: int = 370, height: int = 490, title: str = "rahad@mainframe: ~ (ascii)"):
    num_lines = len(lines)
    start_y = 58
    line_spacing = 9.8
    font_size = 8.6

    css_rules = []
    for i in range(num_lines):
        delay = i * 0.032
        css_rules.append(f".line-{i} {{ animation: fin 0.4s ease-out {delay:.3f}s forwards; opacity: 0; }}")
    css_block = "\n      ".join(css_rules)

    svg_lines = []
    for i, line in enumerate(lines):
        escaped = html.escape(line).replace(" ", "&#160;")
        y_pos = start_y + (i * line_spacing)
        svg_lines.append(f'    <text class="ascii-line line-{i}" x="18" y="{y_pos:.1f}">{escaped}</text>')
    ascii_xml_str = "\n".join(svg_lines)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e0e11" />
      <stop offset="50%" stop-color="#0a0a0c" />
      <stop offset="100%" stop-color="#050507" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37" stop-opacity="0.5" />
      <stop offset="30%" stop-color="#2a2a2e" stop-opacity="0.8" />
      <stop offset="70%" stop-color="#1b1b1f" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0.3" />
    </linearGradient>
    <clipPath id="revealWipe">
      <rect x="0" y="0" width="{width}" height="0">
        <animate attributeName="height" from="0" to="{height}" dur="1.4s" fill="freeze" />
      </rect>
    </clipPath>
  </defs>

  <style>
    @keyframes fin {{
      from {{ opacity: 0; transform: translateY(2px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .ascii-line {{
      font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      font-size: {font_size}px;
      font-weight: 600;
      letter-spacing: 1.8px;
      fill: #D4AF37;
      text-shadow: 0 0 4px rgba(212, 175, 55, 0.35);
      white-space: pre;
    }}
    .terminal-title {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 600;
      fill: #8b949e;
      letter-spacing: 0.5px;
    }}
    .status-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 9px;
      font-weight: 600;
      fill: #10b981;
    }}
    .footer-text {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 9.5px;
      fill: #6e7681;
      letter-spacing: 0.5px;
    }}
    {css_block}
  </style>

  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="url(#cardBg)" stroke="url(#borderGrad)" stroke-width="1.5" />
  <path d="M 1 15 C 1 7.268 7.268 1 15 1 L {width - 15} 1 C {width - 7.268} 1 {width - 1} 7.268 {width - 1} 15 L {width - 1} 38 L 1 38 Z" fill="#141419" />
  <line x1="1" y1="38" x2="{width - 1}" y2="38" stroke="#222228" stroke-width="1" />

  <circle cx="20" cy="19" r="5.5" fill="#ff5f56" stroke="#e0443e" stroke-width="0.5" />
  <circle cx="36" cy="19" r="5.5" fill="#ffbd2e" stroke="#dea123" stroke-width="0.5" />
  <circle cx="52" cy="19" r="5.5" fill="#27c93f" stroke="#1aab29" stroke-width="0.5" />

  <text class="terminal-title" x="{width / 2}" y="23" text-anchor="middle">{title}</text>
  <circle cx="{width - 24}" cy="19" r="3.5" fill="#10b981">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite" />
  </circle>

  <g clip-path="url(#revealWipe)">
{ascii_xml_str}
  </g>

  <line x1="1" y1="{height - 28}" x2="{width - 1}" y2="{height - 28}" stroke="#1f1f26" stroke-width="1" />
  <text class="footer-text" x="18" y="{height - 11}">HEX_ID: 0xRAHAD</text>
  <text class="status-badge" x="{width - 18}" y="{height - 11}" text-anchor="end">+ PORTRAIT V2.0</text>
</svg>'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated ASCII SVG: {output_path} ({width}x{height})")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "hxni-ascii.svg"
    if not os.path.exists(src):
        src = "hero.png" if os.path.exists("hero.png") else src
    lines = image_to_ascii_grid(src, cols=56, rows=41)
    generate_ascii_svg(lines, output_path=out, width=370, height=490)
