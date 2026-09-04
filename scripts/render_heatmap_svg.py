#!/usr/bin/env python3
import sys, os, json, datetime

COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#D4AF37",
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}

def render_heatmap(json_path: str = "data/contributions.json", output_path: str = "contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        import fetch_contributions
        data = fetch_contributions.fetch_github_contributions("rahadalways")
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    days = data.get("days", [])
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"date": "N/A", "count": 0})

    width = 860
    height = 220
    cell_size = 10.5
    cell_gap = 3.2
    start_x = 42
    start_y = 80

    grid_cells_svg = []
    month_labels_svg = []
    last_month = -1

    date_map = {d["date"]: d for d in days}
    end_date = datetime.date.fromisoformat(days[-1]["date"]) if days else datetime.date.today()

    days_to_sat = (5 - end_date.weekday()) % 7
    calendar_end = end_date + datetime.timedelta(days=days_to_sat)
    calendar_start = calendar_end - datetime.timedelta(weeks=52, days=calendar_end.weekday() + 1)

    curr_date = calendar_start
    col_idx = 0

    while col_idx < 53:
        for row_idx in range(7):
            d_str = curr_date.isoformat()
            day_info = date_map.get(d_str, {"count": 0, "level": 0})
            level = day_info.get("level", 0)
            count = day_info.get("count", 0)
            fill_color = COLORS.get(level, COLORS[0])

            x = start_x + col_idx * (cell_size + cell_gap)
            y = start_y + row_idx * (cell_size + cell_gap)

            if row_idx == 0 and curr_date.month != last_month:
                month_labels_svg.append(
                    f'  <text class="month-label" x="{x:.1f}" y="{start_y - 8}">{MONTH_NAMES[curr_date.month - 1]}</text>'
                )
                last_month = curr_date.month

            title_text = f"{count} contributions on {d_str}"
            stroke_attr = ' stroke="#f5e08b" stroke-width="0.8"' if level == 4 else ""
            grid_cells_svg.append(
                f'  <rect class="contrib-cell" x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill_color}"{stroke_attr}><title>{title_text}</title></rect>'
            )

            curr_date += datetime.timedelta(days=1)
        col_idx += 1

    weekday_labels_svg = []
    for r_idx, label in DAY_LABELS.items():
        y_pos = start_y + r_idx * (cell_size + cell_gap) + 8.5
        weekday_labels_svg.append(f'  <text class="day-label" x="22" y="{y_pos:.1f}">{label}</text>')

    cells_str = "\n".join(grid_cells_svg)
    months_str = "\n".join(month_labels_svg)
    days_str = "\n".join(weekday_labels_svg)

    svg_template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 __WIDTH__ __HEIGHT__" width="__WIDTH__" height="__HEIGHT__">
  <defs>
    <linearGradient id="heatBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e0e11" />
      <stop offset="50%" stop-color="#0a0a0c" />
      <stop offset="100%" stop-color="#050507" />
    </linearGradient>

    <linearGradient id="heatBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37" stop-opacity="0.6" />
      <stop offset="35%" stop-color="#2a2a2e" stop-opacity="0.8" />
      <stop offset="70%" stop-color="#1b1b1f" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0.3" />
    </linearGradient>
  </defs>

  <style>
    .card-title {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      fill: #e6edf3;
      letter-spacing: 0.5px;
    }
    .badge-pill {
      font-family: 'JetBrains Mono', 'Segoe UI', monospace;
      font-size: 10px;
      font-weight: 600;
    }
    .month-label, .day-label {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
      font-size: 9.5px;
      fill: #8b949e;
    }
    .legend-text {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
      font-size: 9.5px;
      fill: #8b949e;
    }
  </style>

  <rect x="1" y="1" width="__WIDTH_MIN_2__" height="__HEIGHT_MIN_2__" rx="14" fill="url(#heatBg)" stroke="url(#heatBorder)" stroke-width="1.5" />
  <text class="card-title" x="22" y="32">CONTRIBUTION MATRIX <tspan fill="#D4AF37" font-weight="600">//@rahadalways</tspan></text>

  <g transform="translate(360, 18)">
    <rect x="0" y="0" width="115" height="22" rx="11" fill="#141419" stroke="#D4AF37" stroke-width="0.8" />
    <text class="badge-pill" x="57.5" y="14.5" fill="#D4AF37" text-anchor="middle">TOTAL: __TOTAL__</text>

    <rect x="125" y="0" width="115" height="22" rx="11" fill="#141419" stroke="#10b981" stroke-width="0.8" />
    <text class="badge-pill" x="182.5" y="14.5" fill="#10b981" text-anchor="middle">STREAK: __CURRENT_STREAK__ DAYS</text>

    <rect x="250" y="0" width="115" height="22" rx="11" fill="#141419" stroke="#00f2fe" stroke-width="0.8" />
    <text class="badge-pill" x="307.5" y="14.5" fill="#00f2fe" text-anchor="middle">MAX: __LONGEST_STREAK__ DAYS</text>

    <rect x="375" y="0" width="105" height="22" rx="11" fill="#141419" stroke="#a855f7" stroke-width="0.8" />
    <text class="badge-pill" x="427.5" y="14.5" fill="#a855f7" text-anchor="middle">PEAK: __BEST_DAY_COUNT__/DAY</text>
  </g>

  <line x1="22" y1="48" x2="__WIDTH_MIN_22__" y2="48" stroke="#1f1f26" stroke-width="1" />
__MONTHS_STR__
__DAYS_STR__
__CELLS_STR__

  <g transform="translate(__LEGEND_X__, __LEGEND_Y__)">
    <text class="legend-text" x="-32" y="9.5">Less</text>
    <rect x="0" y="0" width="10" height="10" rx="2" fill="__C0__" />
    <rect x="14" y="0" width="10" height="10" rx="2" fill="__C1__" />
    <rect x="28" y="0" width="10" height="10" rx="2" fill="__C2__" />
    <rect x="42" y="0" width="10" height="10" rx="2" fill="__C3__" />
    <rect x="56" y="0" width="10" height="10" rx="2" fill="__C4__" stroke="#f5e08b" stroke-width="0.6" />
    <text class="legend-text" x="72" y="9.5">More</text>
  </g>

  <circle cx="28" cy="__PULSE_Y__" r="4" fill="#10b981">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
  </circle>
  <text class="legend-text" x="38" y="__PULSE_TEXT_Y__">Live Activity Sync // GitHub Scraper Engine</text>
</svg>"""

    svg_content = (
        svg_template
        .replace("__WIDTH__", str(width))
        .replace("__HEIGHT__", str(height))
        .replace("__WIDTH_MIN_2__", str(width - 2))
        .replace("__HEIGHT_MIN_2__", str(height - 2))
        .replace("__WIDTH_MIN_22__", str(width - 22))
        .replace("__TOTAL__", str(total))
        .replace("__CURRENT_STREAK__", str(current_streak))
        .replace("__LONGEST_STREAK__", str(longest_streak))
        .replace("__BEST_DAY_COUNT__", str(best_day.get('count', 0)))
        .replace("__MONTHS_STR__", months_str)
        .replace("__DAYS_STR__", days_str)
        .replace("__CELLS_STR__", cells_str)
        .replace("__LEGEND_X__", str(width - 170))
        .replace("__LEGEND_Y__", str(height - 24))
        .replace("__C0__", COLORS[0])
        .replace("__C1__", COLORS[1])
        .replace("__C2__", COLORS[2])
        .replace("__C3__", COLORS[3])
        .replace("__C4__", COLORS[4])
        .replace("__PULSE_Y__", str(height - 18))
        .replace("__PULSE_TEXT_Y__", str(height - 15))
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated Heatmap SVG: {output_path} ({width}x{height})")

if __name__ == "__main__":
    in_json = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "contributions.json")
    out_svg = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap(in_json, out_svg)
