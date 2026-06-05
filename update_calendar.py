#!/usr/bin/env python3
"""
WM 2026 Kalender Updater
Holt Ergebnisse von API-Football und aktualisiert WM2026.ics
"""

import os
import re
import requests
from datetime import datetime, timezone, timedelta

# ── Konfiguration ────────────────────────────────────────────────────────────
API_KEY    = os.environ["API_FOOTBALL_KEY"]   # GitHub Secret
LEAGUE_ID  = 1       # FIFA World Cup bei api-sports.io
SEASON     = 2026
ICS_FILE   = "WM2026.ics"
MESZ       = timezone(timedelta(hours=2))     # UTC+2

# ── Flaggen-Emojis ───────────────────────────────────────────────────────────
FLAGS = {
    "Germany":            "🇩🇪",
    "Mexico":             "🇲🇽",
    "South Africa":       "🇿🇦",
    "South Korea":        "🇰🇷",
    "Czech Republic":     "🇨🇿",
    "Canada":             "🇨🇦",
    "Bosnia":             "🇧🇦",
    "Qatar":              "🇶🇦",
    "Switzerland":        "🇨🇭",
    "USA":                "🇺🇸",
    "United States":      "🇺🇸",
    "Paraguay":           "🇵🇾",
    "Australia":          "🇦🇺",
    "Turkey":             "🇹🇷",
    "Brazil":             "🇧🇷",
    "Morocco":            "🇲🇦",
    "Haiti":              "🇭🇹",
    "Scotland":           "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Curacao":            "🇨🇼",
    "Curaçao":            "🇨🇼",
    "Ivory Coast":        "🇨🇮",
    "Ecuador":            "🇪🇨",
    "Netherlands":        "🇳🇱",
    "Japan":              "🇯🇵",
    "Sweden":             "🇸🇪",
    "Tunisia":            "🇹🇳",
    "Belgium":            "🇧🇪",
    "Egypt":              "🇪🇬",
    "Iran":               "🇮🇷",
    "New Zealand":        "🇳🇿",
    "Spain":              "🇪🇸",
    "Cape Verde":         "🇨🇻",
    "Saudi Arabia":       "🇸🇦",
    "Uruguay":            "🇺🇾",
    "France":             "🇫🇷",
    "Senegal":            "🇸🇳",
    "Iraq":               "🇮🇶",
    "Norway":             "🇳🇴",
    "Argentina":          "🇦🇷",
    "Algeria":            "🇩🇿",
    "Austria":            "🇦🇹",
    "Jordan":             "🇯🇴",
    "England":            "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croatia":            "🇭🇷",
    "Colombia":           "🇨🇴",
    "Slovenia":           "🇸🇮",
    "Portugal":           "🇵🇹",
    "Zimbabwe":           "🇿🇼",
    "Sudan":              "🇸🇩",
    "Syria":              "🇸🇾",
    "Korea Republic":     "🇰🇷",
}

def flag(name):
    """Gibt Flaggen-Emoji für ein Land zurück, oder ⚽ als Fallback."""
    for key, emoji in FLAGS.items():
        if key.lower() in name.lower() or name.lower() in key.lower():
            return emoji
    return "⚽"

def get_fixtures():
    """Holt alle WM-Spiele von API-Football."""
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params  = {"league": LEAGUE_ID, "season": SEASON}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    print(f"API-Antwort: {data['results']} Spiele gefunden")
    return data["response"]

def fixture_to_event(f):
    """Konvertiert ein API-Fixture in ein iCal VEVENT."""
    home    = f["teams"]["home"]["name"]
    away    = f["teams"]["away"]["name"]
    goals_h = f["goals"]["home"]
    goals_a = f["goals"]["away"]
    status  = f["fixture"]["status"]["short"]  # FT, NS, 1H, 2H, HT, ...
    venue   = f["fixture"]["venue"]["name"] or ""
    city    = f["fixture"]["venue"]["city"] or ""
    uid     = f"wm2026-api-{f['fixture']['id']}@wm2026"
    round_  = f["league"]["round"]

    # Datum / Uhrzeit
    dt_utc = datetime.fromisoformat(
        f["fixture"]["date"].replace("Z", "+00:00")
    )
    dt_mesz = dt_utc.astimezone(MESZ)
    dt_end  = dt_mesz + timedelta(hours=2)

    dtstart = dt_mesz.strftime("%Y%m%dT%H%M%S")
    dtend   = dt_end.strftime("%Y%m%dT%H%M%S")

    # Titel mit Flaggen
    fh = flag(home)
    fa = flag(away)

    if status == "FT" and goals_h is not None and goals_a is not None:
        # Spiel beendet → Ergebnis anzeigen
        summary = f"{fh} {home} {goals_h}:{goals_a} {fa} {away}"
    elif status in ("1H", "2H", "HT", "ET", "P"):
        # Spiel läuft
        g_h = goals_h if goals_h is not None else 0
        g_a = goals_a if goals_a is not None else 0
        summary = f"🔴 {fh} {home} {g_h}:{g_a} {fa} {away} (LIVE)"
    else:
        # Noch nicht gespielt
        summary = f"{fh} {home} vs {fa} {away}"

    # Runde als Beschreibung
    description = f"FIFA WM 2026 - {round_}"

    return (
        "BEGIN:VEVENT\n"
        f"UID:{uid}\n"
        f"SUMMARY:{summary}\n"
        f"DTSTART;TZID=Europe/Berlin:{dtstart}\n"
        f"DTEND;TZID=Europe/Berlin:{dtend}\n"
        f"LOCATION:{venue}, {city}\n"
        f"DESCRIPTION:{description}\n"
        "END:VEVENT"
    )

def build_ics(fixtures):
    """Baut die komplette .ics-Datei aus den Fixtures."""
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    header = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//WM 2026 Auto-Update//DE\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:PUBLISH\n"
        "X-WR-CALNAME:⚽ WM 2026 Spielplan\n"
        "X-WR-TIMEZONE:Europe/Berlin\n"
        f"X-WR-CALDESC:Automatisch aktualisiert am {now} UTC\n"
    )
    footer = "END:VCALENDAR\n"

    events = "\n\n".join(fixture_to_event(f) for f in fixtures)
    return header + "\n" + events + "\n\n" + footer

def main():
    print("🔄 Lade WM-Spielplan von API-Football...")
    fixtures = get_fixtures()
    print(f"✅ {len(fixtures)} Spiele geladen")

    print("📅 Baue ICS-Datei...")
    ics_content = build_ics(fixtures)

    with open(ICS_FILE, "w", encoding="utf-8") as f:
        f.write(ics_content)

    print(f"✅ {ICS_FILE} gespeichert ({len(ics_content)} Zeichen)")

if __name__ == "__main__":
    main()
