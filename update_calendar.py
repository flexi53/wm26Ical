#!/usr/bin/env python3
"""WM 2026 Kalender Updater – holt Ergebnisse von API-Football und schreibt WM2026.ics"""

import os
import requests
from datetime import datetime, timezone, timedelta

API_KEY   = os.environ["API_FOOTBALL_KEY"]
LEAGUE_ID = 1
SEASON    = 2026
ICS_FILE  = "WM2026.ics"
MESZ      = timezone(timedelta(hours=2))  # UTC+2, gilt für gesamte WM (Jun–Jul)

# ── Flaggen-Emojis (alle 48 WM-2026-Teilnehmer + API-Varianten) ──────────────
FLAGS = {
    # Europa
    "Germany":            "🇩🇪",
    "Spain":              "🇪🇸",
    "France":             "🇫🇷",
    "Portugal":           "🇵🇹",
    "England":            "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Netherlands":        "🇳🇱",
    "Belgium":            "🇧🇪",
    "Croatia":            "🇭🇷",
    "Austria":            "🇦🇹",
    "Turkey":             "🇹🇷",
    "Scotland":           "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Serbia":             "🇷🇸",
    "Czech Republic":     "🇨🇿",
    "Switzerland":        "🇨🇭",
    "Hungary":            "🇭🇺",
    "Slovenia":           "🇸🇮",
    "Romania":            "🇷🇴",
    "Greece":             "🇬🇷",
    "Albania":            "🇦🇱",
    "Slovakia":           "🇸🇰",
    "Ukraine":            "🇺🇦",
    "Wales":              "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Denmark":            "🇩🇰",
    "Poland":             "🇵🇱",
    "Italy":              "🇮🇹",
    "Bosnia":             "🇧🇦",
    "Norway":             "🇳🇴",
    "Sweden":             "🇸🇪",
    # CONCACAF
    "USA":                "🇺🇸",
    "United States":      "🇺🇸",
    "Mexico":             "🇲🇽",
    "Canada":             "🇨🇦",
    "Panama":             "🇵🇦",
    "Honduras":           "🇭🇳",
    "Costa Rica":         "🇨🇷",
    "Jamaica":            "🇯🇲",
    "El Salvador":        "🇸🇻",
    "Haiti":              "🇭🇹",
    "Curacao":            "🇨🇼",
    "Curaçao":            "🇨🇼",
    "Trinidad":           "🇹🇹",
    "Guatemala":          "🇬🇹",
    # CONMEBOL
    "Argentina":          "🇦🇷",
    "Brazil":             "🇧🇷",
    "Colombia":           "🇨🇴",
    "Ecuador":            "🇪🇨",
    "Uruguay":            "🇺🇾",
    "Venezuela":          "🇻🇪",
    "Paraguay":           "🇵🇾",
    "Bolivia":            "🇧🇴",
    "Chile":              "🇨🇱",
    "Peru":               "🇵🇪",
    # Afrika
    "Morocco":            "🇲🇦",
    "Senegal":            "🇸🇳",
    "Egypt":              "🇪🇬",
    "Ivory Coast":        "🇨🇮",
    "Nigeria":            "🇳🇬",
    "Cameroon":           "🇨🇲",
    "South Africa":       "🇿🇦",
    "Tunisia":            "🇹🇳",
    "Algeria":            "🇩🇿",
    "DR Congo":           "🇨🇩",
    "Congo":              "🇨🇩",
    "Cape Verde":         "🇨🇻",
    "Mali":               "🇲🇱",
    "Zambia":             "🇿🇲",
    "Angola":             "🇦🇴",
    "Tanzania":           "🇹🇿",
    "Zimbabwe":           "🇿🇼",
    "Sudan":              "🇸🇩",
    "Comoros":            "🇰🇲",
    "Benin":              "🇧🇯",
    # Asien
    "Japan":              "🇯🇵",
    "South Korea":        "🇰🇷",
    "Korea Republic":     "🇰🇷",
    "Iran":               "🇮🇷",
    "Saudi Arabia":       "🇸🇦",
    "Australia":          "🇦🇺",
    "Qatar":              "🇶🇦",
    "Iraq":               "🇮🇶",
    "Jordan":             "🇯🇴",
    "Uzbekistan":         "🇺🇿",
    "Bahrain":            "🇧🇭",
    "Indonesia":          "🇮🇩",
    "China":              "🇨🇳",
    "Syria":              "🇸🇾",
    "Oman":               "🇴🇲",
    "Kuwait":             "🇰🇼",
    # Ozeanien
    "New Zealand":        "🇳🇿",
    "Fiji":               "🇫🇯",
    "Papua New Guinea":   "🇵🇬",
    "Vanuatu":            "🇻🇺",
}

# ── Deutsche Rundenbezeichnungen ──────────────────────────────────────────────
ROUND_DE = {
    "Group Stage - 1":  "Vorrunde – 1. Spieltag",
    "Group Stage - 2":  "Vorrunde – 2. Spieltag",
    "Group Stage - 3":  "Vorrunde – 3. Spieltag",
    "Round of 32":      "Runde der letzten 32",
    "Round of 16":      "Achtelfinale",
    "Quarter-finals":   "Viertelfinale",
    "Semi-finals":      "Halbfinale",
    "3rd Place Final":  "Spiel um Platz 3",
    "Final":            "Finale",
}

# ── UTC-Offset der Spielorte im Sommer 2026 ───────────────────────────────────
# Vollständige Adressen der Spielstätten (für Apple Maps)
VENUE_ADDRESS = {
    "Estadio Azteca":          "Estadio Azteca, Ciudad de México, Mexiko",
    "Estadio Akron":           "Estadio Akron, Guadalajara, Mexiko",
    "Estadio BBVA":            "Estadio BBVA, Monterrey, Mexiko",
    "BMO Field":               "BMO Field, Toronto, Kanada",
    "BC Place":                "BC Place, Vancouver, Kanada",
    "Levi's Stadium":          "Levi's Stadium, Santa Clara, USA",
    "SoFi Stadium":            "SoFi Stadium, Inglewood, Los Angeles, USA",
    "MetLife Stadium":         "MetLife Stadium, East Rutherford, New York, USA",
    "Gillette Stadium":        "Gillette Stadium, Foxborough, Boston, USA",
    "NRG Stadium":             "NRG Stadium, Houston, USA",
    "AT&T Stadium":            "AT&T Stadium, Arlington, Dallas, USA",
    "Lincoln Financial Field": "Lincoln Financial Field, Philadelphia, USA",
    "Mercedes-Benz Stadium":   "Mercedes-Benz Stadium, Atlanta, USA",
    "Lumen Field":             "Lumen Field, Seattle, USA",
    "Hard Rock Stadium":       "Hard Rock Stadium, Miami Gardens, Miami, USA",
    "Arrowhead Stadium":       "Arrowhead Stadium, Kansas City, USA",
}


def full_address(venue: str, city: str) -> str:
    for key, addr in VENUE_ADDRESS.items():
        if key.lower() in venue.lower():
            return addr
    return f"{venue}, {city}" if venue and city else venue or city


CITY_OFFSET = {
    # USA Ostküste (EDT = UTC−4)
    "New York":        -4,
    "East Rutherford": -4,
    "Boston":          -4,
    "Miami":           -4,
    "Atlanta":         -4,
    "Philadelphia":    -4,
    "Baltimore":       -4,
    # USA Mitte (CDT = UTC−5)
    "Dallas":          -5,
    "Kansas City":     -5,
    "Houston":         -5,
    # USA Westküste (PDT = UTC−7)
    "Los Angeles":     -7,
    "Inglewood":       -7,
    "San Francisco":   -7,
    "Santa Clara":     -7,
    "Seattle":         -7,
    "Vancouver":       -7,
    # Kanada Ostküste (EDT = UTC−4)
    "Toronto":         -4,
    # Mexiko (CDT = UTC−5)
    "Mexico City":     -5,
    "Guadalajara":     -5,
    "Monterrey":       -5,
}


def flag(name: str) -> str:
    for key, emoji in FLAGS.items():
        if key.lower() in name.lower() or name.lower() in key.lower():
            return emoji
    return "⚽"


def round_de(round_str: str) -> str:
    if round_str in ROUND_DE:
        return ROUND_DE[round_str]
    for key, val in ROUND_DE.items():
        if round_str.lower().startswith(key.lower()):
            return val
    return round_str


def local_time_str(dt_utc: datetime, city: str) -> str | None:
    offset = CITY_OFFSET.get(city)
    if offset is None:
        for key, off in CITY_OFFSET.items():
            if key.lower() in city.lower():
                offset = off
                break
    if offset is None:
        return None
    local_dt = dt_utc + timedelta(hours=offset)
    sign = "−" if offset < 0 else "+"
    return f"{local_dt.strftime('%H:%M')} Uhr (UTC{sign}{abs(offset)})"


def ical_escape(text: str) -> str:
    return (text
            .replace("\\", "\\\\")
            .replace(";",  "\\;")
            .replace(",",  "\\,")
            .replace("\n", "\\n"))


def fold(line: str) -> str:
    """RFC 5545 line folding at 75 octets."""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line
    parts = []
    while len(line.encode("utf-8")) > 75:
        n = 75
        while len(line[:n].encode("utf-8")) > 75:
            n -= 1
        parts.append(line[:n])
        line = " " + line[n:]
    parts.append(line)
    return "\r\n".join(parts)


def get_fixtures() -> list:
    r = requests.get(
        "https://v3.football.api-sports.io/fixtures",
        headers={"x-apisports-key": API_KEY},
        params={"league": LEAGUE_ID, "season": SEASON},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    print(f"API: {data['results']} Spiele geladen")
    return data["response"]


def fixture_to_event(f: dict) -> str:
    home    = f["teams"]["home"]["name"]
    away    = f["teams"]["away"]["name"]
    goals_h = f["goals"]["home"]
    goals_a = f["goals"]["away"]
    status  = f["fixture"]["status"]["short"]
    elapsed = f["fixture"]["status"].get("elapsed")
    venue   = (f["fixture"]["venue"]["name"] or "").strip()
    city    = (f["fixture"]["venue"]["city"] or "").strip()
    uid     = f"wm2026-{f['fixture']['id']}@wm2026"
    round_  = f["league"]["round"]
    group   = (f["league"].get("group") or "").strip()

    dt_utc  = datetime.fromisoformat(f["fixture"]["date"].replace("Z", "+00:00"))
    dt_mesz = dt_utc.astimezone(MESZ)
    dt_end  = dt_mesz + timedelta(hours=2)
    dtstart = dt_mesz.strftime("%Y%m%dT%H%M%S")
    dtend   = dt_end.strftime("%Y%m%dT%H%M%S")
    mesz_str = dt_mesz.strftime("%H:%M")

    fh = flag(home)
    fa = flag(away)

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    if status in ("FT", "AET", "PEN") and goals_h is not None:
        suffix = " n.V." if status == "AET" else " n.E." if status == "PEN" else ""
        summary = f"{fh} {home} {goals_h}:{goals_a} {fa} {away}{suffix}"
    elif status in ("1H", "2H", "HT", "ET", "BT", "P", "LIVE"):
        g_h = goals_h or 0
        g_a = goals_a or 0
        min_str = f" {elapsed}'" if elapsed else ""
        summary = f"🔴 LIVE{min_str} {fh} {home} {g_h}:{g_a} {fa} {away}"
    elif status == "PST":
        summary = f"⏸️ {fh} {home} vs {fa} {away} (Verlegt)"
    elif status == "CANC":
        summary = f"❌ {fh} {home} vs {fa} {away} (Abgesagt)"
    else:
        summary = f"{fh} {home} vs {fa} {away}"

    # ── DESCRIPTION ───────────────────────────────────────────────────────────
    runde    = round_de(round_)
    local_t  = local_time_str(dt_utc, city)
    location = full_address(venue, city)

    desc_lines = [f"⚽ FIFA WM 2026 – {runde}"]
    if group:
        desc_lines.append(f"📊 {group}")
    desc_lines.append("")
    if venue:
        desc_lines.append(f"🏟️  {venue}")
    if city:
        desc_lines.append(f"📍 {city}")
    desc_lines.append("")
    if local_t:
        desc_lines.append(f"⏰ Anstoß: {mesz_str} Uhr (MESZ) / {local_t}")
    else:
        desc_lines.append(f"⏰ Anstoß: {mesz_str} Uhr (MESZ)")

    if status in ("FT", "AET", "PEN") and goals_h is not None:
        suffix = " (n.V.)" if status == "AET" else " (n.E.)" if status == "PEN" else ""
        desc_lines += ["", f"✅ Endstand: {goals_h}:{goals_a}{suffix}"]
    elif status in ("1H", "2H", "HT", "ET", "BT", "P", "LIVE"):
        min_str = f" ({elapsed}')" if elapsed else ""
        desc_lines += ["", f"🔴 Spiel läuft{min_str}"]

    description = ical_escape("\n".join(desc_lines))

    lines = [
        "BEGIN:VEVENT",
        fold(f"UID:{uid}"),
        fold(f"SUMMARY:{summary}"),
        f"DTSTART;TZID=Europe/Berlin:{dtstart}",
        f"DTEND;TZID=Europe/Berlin:{dtend}",
        fold(f"LOCATION:{location}"),
        fold(f"DESCRIPTION:{description}"),
        # 30-Minuten-Erinnerung vor Anstoß
        "BEGIN:VALARM",
        "TRIGGER:-PT30M",
        "ACTION:DISPLAY",
        "DESCRIPTION:Anstoß in 30 Minuten!",
        "END:VALARM",
        "END:VEVENT",
    ]
    return "\r\n".join(lines)


VTIMEZONE = "\r\n".join([
    "BEGIN:VTIMEZONE",
    "TZID:Europe/Berlin",
    "BEGIN:STANDARD",
    "DTSTART:19701025T030000",
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10",
    "TZNAME:MEZ",
    "TZOFFSETFROM:+0200",
    "TZOFFSETTO:+0100",
    "END:STANDARD",
    "BEGIN:DAYLIGHT",
    "DTSTART:19700329T020000",
    "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3",
    "TZNAME:MESZ",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0200",
    "END:DAYLIGHT",
    "END:VTIMEZONE",
])


def build_ics(fixtures: list) -> str:
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    header = "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//WM 2026 Auto-Update//DE",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:⚽ WM 2026 Spielplan",
        "X-WR-TIMEZONE:Europe/Berlin",
        f"X-WR-CALDESC:Automatisch aktualisiert am {now} UTC",
    ])
    footer = "END:VCALENDAR"
    events = "\r\n".join(fixture_to_event(f) for f in fixtures)
    return header + "\r\n" + VTIMEZONE + "\r\n" + events + "\r\n" + footer + "\r\n"


def main():
    print("🔄 Lade WM-Spielplan von API-Football...")
    fixtures = get_fixtures()
    print(f"✅ {len(fixtures)} Spiele geladen")

    print("📅 Baue ICS-Datei...")
    ics_content = build_ics(fixtures)

    with open(ICS_FILE, "wb") as fh:
        fh.write(ics_content.encode("utf-8"))

    print(f"✅ {ICS_FILE} gespeichert ({len(ics_content):,} Zeichen)")


if __name__ == "__main__":
    main()
