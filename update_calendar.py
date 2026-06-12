#!/usr/bin/env python3
"""WM 2026 Kalender Updater – football-data.org API"""

import os
import requests
from datetime import datetime, timezone, timedelta

API_KEY  = os.environ["FOOTBALL_DATA_KEY"]
BASE_URL = "https://api.football-data.org/v4"
ICS_FILE = "WM2026.ics"
MESZ     = timezone(timedelta(hours=2))

# ── Flaggen-Emojis ────────────────────────────────────────────────────────────
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
    "Czechia":            "🇨🇿",
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
    "Côte d'Ivoire":      "🇨🇮",
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

# ── Vollständige Adressen der Spielstätten ────────────────────────────────────
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
    "Allegiant Stadium":       "Allegiant Stadium, Las Vegas, USA",
}

# ── Spielpaarung → Stadion (football-data.org Teamnamen) ─────────────────────
MATCH_VENUES = {
    # Gruppe A
    ("Mexico", "South Africa"):            "Estadio Azteca",
    ("South Korea", "Czechia"):            "Estadio Akron",
    ("Mexico", "South Korea"):             "Estadio Akron",
    ("Czechia", "South Africa"):           "Mercedes-Benz Stadium",
    ("South Africa", "South Korea"):       "Estadio BBVA",
    ("Czechia", "Mexico"):                 "Estadio Azteca",
    # Gruppe B
    ("Canada", "Bosnia-Herzegovina"):      "BMO Field",
    ("Qatar", "Switzerland"):              "Levi's Stadium",
    ("Switzerland", "Bosnia-Herzegovina"): "SoFi Stadium",
    ("Canada", "Qatar"):                   "BC Place",
    ("Switzerland", "Canada"):             "BC Place",
    ("Bosnia-Herzegovina", "Qatar"):       "Lumen Field",
    # Gruppe C
    ("Brazil", "Morocco"):                 "MetLife Stadium",
    ("Haiti", "Scotland"):                 "Gillette Stadium",
    ("Scotland", "Morocco"):               "Gillette Stadium",
    ("Brazil", "Haiti"):                   "Lincoln Financial Field",
    ("Scotland", "Brazil"):                "Hard Rock Stadium",
    ("Morocco", "Haiti"):                  "Mercedes-Benz Stadium",
    # Gruppe D
    ("United States", "Paraguay"):         "SoFi Stadium",
    ("Australia", "Turkey"):               "BC Place",
    ("Turkey", "Paraguay"):                "Levi's Stadium",
    ("United States", "Australia"):        "Lumen Field",
    ("Paraguay", "Australia"):             "Levi's Stadium",
    ("Turkey", "United States"):           "SoFi Stadium",
    # Gruppe E
    ("Germany", "Curaçao"):                "NRG Stadium",
    ("Ivory Coast", "Ecuador"):            "Lincoln Financial Field",
    ("Germany", "Ivory Coast"):            "BMO Field",
    ("Ecuador", "Curaçao"):               "Arrowhead Stadium",
    ("Ecuador", "Germany"):               "MetLife Stadium",
    ("Curaçao", "Ivory Coast"):           "Lincoln Financial Field",
    # Gruppe F
    ("Netherlands", "Japan"):             "AT&T Stadium",
    ("Sweden", "Tunisia"):                "Estadio BBVA",
    ("Netherlands", "Sweden"):            "NRG Stadium",
    ("Tunisia", "Japan"):                 "Estadio BBVA",
    ("Japan", "Sweden"):                  "AT&T Stadium",
    ("Tunisia", "Netherlands"):           "Arrowhead Stadium",
    # Gruppe G
    ("Belgium", "Egypt"):                 "Lumen Field",
    ("Iran", "New Zealand"):              "SoFi Stadium",
    ("Belgium", "Iran"):                  "SoFi Stadium",
    ("New Zealand", "Egypt"):             "BC Place",
    ("New Zealand", "Belgium"):           "BC Place",
    ("Egypt", "Iran"):                    "Lumen Field",
    # Gruppe H
    ("Spain", "Cape Verde Islands"):      "Mercedes-Benz Stadium",
    ("Saudi Arabia", "Uruguay"):          "Hard Rock Stadium",
    ("Uruguay", "Cape Verde Islands"):    "Hard Rock Stadium",
    ("Spain", "Saudi Arabia"):            "Mercedes-Benz Stadium",
    ("Uruguay", "Spain"):                 "Estadio Akron",
    ("Cape Verde Islands", "Saudi Arabia"): "NRG Stadium",
    # Gruppe I
    ("France", "Senegal"):                "MetLife Stadium",
    ("Iraq", "Norway"):                   "Gillette Stadium",
    ("Norway", "Senegal"):                "MetLife Stadium",
    ("France", "Iraq"):                   "Lincoln Financial Field",
    ("Norway", "France"):                 "Gillette Stadium",
    ("Senegal", "Iraq"):                  "BMO Field",
    # Gruppe J
    ("Argentina", "Algeria"):             "Arrowhead Stadium",
    ("Austria", "Jordan"):                "Levi's Stadium",
    ("Argentina", "Austria"):             "AT&T Stadium",
    ("Jordan", "Algeria"):                "Levi's Stadium",
    ("Austria", "Algeria"):               "Allegiant Stadium",
    ("Jordan", "Argentina"):              "Levi's Stadium",
    # Gruppe K
    ("Portugal", "Zimbabwe"):             "Allegiant Stadium",
    ("Colombia", "Slovenia"):             "Hard Rock Stadium",
    ("Portugal", "Slovenia"):             "Allegiant Stadium",
    ("Colombia", "Zimbabwe"):             "NRG Stadium",
    ("Portugal", "Colombia"):             "Allegiant Stadium",
    ("Zimbabwe", "Slovenia"):             "NRG Stadium",
    # Gruppe L
    ("England", "Croatia"):               "AT&T Stadium",
    ("England", "Sudan"):                 "Hard Rock Stadium",
    ("Croatia", "Syria"):                 "Gillette Stadium",
    ("England", "Syria"):                 "AT&T Stadium",
    ("Croatia", "Sudan"):                 "Gillette Stadium",
    ("Sudan", "England"):                 "Gillette Stadium",
}

# ── KO-Spiele: Anstoßzeit (MESZ) → Stadion (für TBD-Teams) ──────────────────
KO_VENUES = {
    "20260628T210000": "MetLife Stadium",
    "20260629T000000": "Hard Rock Stadium",
    "20260629T210000": "AT&T Stadium",
    "20260630T000000": "Lincoln Financial Field",
    "20260630T210000": "Mercedes-Benz Stadium",
    "20260701T000000": "SoFi Stadium",
    "20260701T210000": "Levi's Stadium",
    "20260702T000000": "Lumen Field",
    "20260702T210000": "BC Place",
    "20260703T000000": "BMO Field",
    "20260703T210000": "Arrowhead Stadium",
    "20260704T000000": "Allegiant Stadium",
    "20260704T210000": "NRG Stadium",
    "20260705T000000": "Estadio Azteca",
    "20260705T210000": "Gillette Stadium",
    "20260706T000000": "MetLife Stadium",
    "20260707T210000": "Hard Rock Stadium",
    "20260708T010000": "SoFi Stadium",
    "20260708T210000": "AT&T Stadium",
    "20260709T010000": "MetLife Stadium",
    "20260709T210000": "Levi's Stadium",
    "20260710T010000": "Lumen Field",
    "20260710T210000": "BC Place",
    "20260711T010000": "NRG Stadium",
    "20260714T210000": "Mercedes-Benz Stadium",
    "20260715T010000": "SoFi Stadium",
    "20260715T210000": "MetLife Stadium",
    "20260716T010000": "AT&T Stadium",
    "20260718T210000": "Hard Rock Stadium",
    "20260719T210000": "MetLife Stadium",
}

# ── UTC-Offset der Spielorte im Sommer 2026 ───────────────────────────────────
CITY_OFFSET = {
    "New York":        -4,
    "East Rutherford": -4,
    "Boston":          -4,
    "Foxborough":      -4,
    "Miami":           -4,
    "Miami Gardens":   -4,
    "Atlanta":         -4,
    "Philadelphia":    -4,
    "Dallas":          -5,
    "Arlington":       -5,
    "Kansas City":     -5,
    "Houston":         -5,
    "Las Vegas":       -7,
    "Los Angeles":     -7,
    "Inglewood":       -7,
    "San Francisco":   -7,
    "Santa Clara":     -7,
    "Seattle":         -7,
    "Vancouver":       -7,
    "Toronto":         -4,
    "Mexico City":     -5,
    "Ciudad de México": -5,
    "Guadalajara":     -5,
    "Monterrey":       -5,
}

# ── Runden auf Deutsch ────────────────────────────────────────────────────────
STAGE_DE = {
    "GROUP_STAGE":        "Vorrunde",
    "LAST_32":            "Runde der letzten 32",
    "LAST_16":            "Achtelfinale",
    "QUARTER_FINALS":     "Viertelfinale",
    "SEMI_FINALS":        "Halbfinale",
    "THIRD_PLACE":        "Spiel um Platz 3",
    "FINAL":              "Finale",
}

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


def flag(name: str) -> str:
    if not name:
        return "⚽"
    for key, emoji in FLAGS.items():
        if key.lower() in name.lower() or name.lower() in key.lower():
            return emoji
    return "⚽"


def get_venue(home: str, away: str, dtstart: str) -> str:
    """Venue aus Paarung oder KO-Datum ermitteln."""
    key = MATCH_VENUES.get((home, away))
    if not key:
        h, a = home.lower(), away.lower()
        for (mh, ma), v in MATCH_VENUES.items():
            if (mh.lower() in h or h in mh.lower()) and (ma.lower() in a or a in ma.lower()):
                key = v
                break
    if not key:
        key = KO_VENUES.get(dtstart)
    return VENUE_ADDRESS.get(key, "") if key else ""


def local_time_str(dt_utc: datetime, address: str) -> str | None:
    offset = None
    for city, off in CITY_OFFSET.items():
        if city.lower() in address.lower():
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
    if len(line.encode("utf-8")) <= 75:
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


def get_matches() -> list:
    r = requests.get(
        f"{BASE_URL}/competitions/WC/matches",
        headers={"X-Auth-Token": API_KEY},
        params={"season": 2026},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    matches = data.get("matches", [])
    print(f"API: {len(matches)} Spiele geladen")
    return matches


def match_to_event(m: dict) -> str:
    home   = m["homeTeam"]["name"] or m["homeTeam"].get("shortName") or "TBD"
    away   = m["awayTeam"]["name"] or m["awayTeam"].get("shortName") or "TBD"
    status = m["status"]  # SCHEDULED, TIMED, IN_PLAY, PAUSED, FINISHED, POSTPONED, CANCELLED
    stage  = m.get("stage", "")
    group  = m.get("group") or ""
    matchday = m.get("matchday")
    venue  = m.get("venue") or ""
    uid    = f"wm2026-fd-{m['id']}@wm2026"

    score    = m.get("score", {})
    ft       = score.get("fullTime", {})
    goals_h  = ft.get("home")
    goals_a  = ft.get("away")
    duration = score.get("duration", "REGULAR")

    dt_utc  = datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
    dt_mesz = dt_utc.astimezone(MESZ)
    dt_end  = dt_mesz + timedelta(hours=2)
    dtstart = dt_mesz.strftime("%Y%m%dT%H%M%S")
    dtend   = dt_end.strftime("%Y%m%dT%H%M%S")
    mesz_str = dt_mesz.strftime("%H:%M")
    address = get_venue(home, away, dtstart)

    fh = flag(home)
    fa = flag(away)

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    if status == "FINISHED" and goals_h is not None:
        suffix = " n.V." if duration == "EXTRA_TIME" else " n.E." if duration == "PENALTY_SHOOTOUT" else ""
        summary = f"{fh} {home} {goals_h}:{goals_a} {fa} {away}{suffix}"
    elif status in ("IN_PLAY", "PAUSED"):
        g_h = goals_h or 0
        g_a = goals_a or 0
        summary = f"🔴 LIVE {fh} {home} {g_h}:{g_a} {fa} {away}"
    elif status == "POSTPONED":
        summary = f"⏸️ {fh} {home} vs {fa} {away} (Verlegt)"
    elif status == "CANCELLED":
        summary = f"❌ {fh} {home} vs {fa} {away} (Abgesagt)"
    else:
        summary = f"{fh} {home} vs {fa} {away}"

    # ── DESCRIPTION ───────────────────────────────────────────────────────────
    stage_de = STAGE_DE.get(stage, stage)
    if stage == "GROUP_STAGE" and group:
        group_label = group.replace("GROUP_", "Gruppe ")
        stage_de = f"Vorrunde – {group_label}"
        if matchday:
            stage_de += f", Spieltag {matchday}"

    local_t = local_time_str(dt_utc, address)

    desc_lines = [f"⚽ FIFA WM 2026 – {stage_de}", ""]
    if address:
        desc_lines.append(f"🏟️  {address}")
    elif venue:
        desc_lines.append(f"🏟️  {venue}")
    desc_lines.append("")
    if local_t:
        desc_lines.append(f"⏰ Anstoß: {mesz_str} Uhr (MESZ) / {local_t}")
    else:
        desc_lines.append(f"⏰ Anstoß: {mesz_str} Uhr (MESZ)")

    if status == "FINISHED" and goals_h is not None:
        suffix = " (n.V.)" if duration == "EXTRA_TIME" else " (n.E.)" if duration == "PENALTY_SHOOTOUT" else ""
        desc_lines += ["", f"✅ Endstand: {goals_h}:{goals_a}{suffix}"]
    elif status in ("IN_PLAY", "PAUSED"):
        desc_lines += ["", "🔴 Spiel läuft"]

    description = ical_escape("\n".join(desc_lines))

    lines = [
        "BEGIN:VEVENT",
        fold(f"UID:{uid}"),
        fold(f"SUMMARY:{summary}"),
        f"DTSTART;TZID=Europe/Berlin:{dtstart}",
        f"DTEND;TZID=Europe/Berlin:{dtend}",
        fold(f"LOCATION:{address}"),
        fold(f"DESCRIPTION:{description}"),
        "URL:https://web.magentatv.de",
        "BEGIN:VALARM",
        "TRIGGER:-PT30M",
        "ACTION:DISPLAY",
        "DESCRIPTION:Anstoß in 30 Minuten!",
        "END:VALARM",
        "END:VEVENT",
    ]
    return "\r\n".join(lines)


def build_ics(matches: list) -> str:
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
    events = "\r\n".join(match_to_event(m) for m in matches)
    return header + "\r\n" + VTIMEZONE + "\r\n" + events + "\r\nEND:VCALENDAR\r\n"


def main():
    print("🔄 Lade WM-Spielplan von football-data.org...")
    matches = get_matches()

    if not matches:
        print("⚠️  Keine Spiele von der API – Datei wird nicht überschrieben.")
        return

    print("📅 Baue ICS-Datei...")
    ics_content = build_ics(matches)

    with open(ICS_FILE, "wb") as fh:
        fh.write(ics_content.encode("utf-8"))

    print(f"✅ {ICS_FILE} gespeichert ({len(ics_content):,} Zeichen)")


if __name__ == "__main__":
    main()
