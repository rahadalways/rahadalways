#!/usr/bin/env python3
import sys, os, re, json, datetime, requests
from bs4 import BeautifulSoup

DEFAULT_USER = "rahadalways"

def fetch_github_contributions(username: str = DEFAULT_USER) -> dict:
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"[*] Fetching contributions from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"[!] Warning during fetch: {e}")
        soup = BeautifulSoup("", "html.parser")

    days_data = []
    cells = soup.find_all("td", class_="ContributionCalendar-day")
    tooltips = {}
    for tip in soup.find_all("tool-tip"):
        tip_for = tip.get("for")
        if tip_for:
            tooltips[tip_for] = tip.get_text(strip=True)

    for cell in cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue
        level = int(cell.get("data-level", 0))
        cell_id = cell.get("id")

        count = 0
        tooltip_text = tooltips.get(cell_id, "")
        if not tooltip_text:
            tooltip_text = cell.get_text(strip=True)

        match = re.search(r"(\d+)\s+contribution", tooltip_text, re.IGNORECASE)
        if match:
            count = int(match.group(1))
        elif "no contribution" in tooltip_text.lower():
            count = 0
        elif level > 0:
            count = max(1, level)

        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })

    if not days_data:
        print("[!] Synthesizing 365-day calendar...")
        today = datetime.date.today()
        for i in range(365, -1, -1):
            d = today - datetime.timedelta(days=i)
            days_data.append({
                "date": d.isoformat(),
                "count": 0,
                "level": 0
            })

    days_data.sort(key=lambda x: x["date"])
    total_contributions = sum(d["count"] for d in days_data)
    best_day = max(days_data, key=lambda x: x["count"]) if days_data else {"date": "N/A", "count": 0}

    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    for day in days_data:
        if day["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    for day in reversed(days_data):
        if day["count"] > 0:
            current_streak += 1
        else:
            if day["date"] == datetime.date.today().isoformat() and current_streak == 0:
                continue
            break

    result = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {
            "date": best_day["date"],
            "count": best_day["count"]
        },
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "days": days_data
    }
    return result

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USER
    out_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join("data", "contributions.json")

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    data = fetch_github_contributions(username)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[+] Saved contributions to {out_file}: Total={data['total_contributions']}, Streak={data['current_streak']}d, Max={data['longest_streak']}d, Peak={data['best_day']['count']}")

if __name__ == "__main__":
    main()
