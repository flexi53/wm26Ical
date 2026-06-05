# ⚽ WM 2026 iCal Kalender

Automatisch aktualisierter Kalender für alle 104 Spiele der FIFA Weltmeisterschaft 2026 – mit Flaggen-Emojis und Ergebnissen.

## 📅 Kalender abonnieren

```
https://raw.githubusercontent.com/flexi53/wm26Ical/main/WM2026.ics
```

Diesen Link als **iCal-Abonnement** in deiner Kalender-App eintragen:

- **iPhone/iPad:** Einstellungen → Kalender → Accounts → Account hinzufügen → Andere → Kalenderabo hinzufügen
- **Mac:** Kalender.app → Ablage → Neues Kalenderabonnement
- **Google Kalender:** Andere Kalender → Per URL

## ✨ Features

- 🏳️ Alle Länder mit Flaggen-Emojis im Titel
- ✅ Ergebnisse werden automatisch eingetragen (`🇩🇪 Deutschland 4:0 🇨🇼 Curaçao`)
- 🔴 Laufende Spiele werden als LIVE markiert
- ⚽ KO-Runde: Teams werden automatisch eingetragen sobald sie feststehen
- 🕐 Alle Zeiten in **MESZ (deutsche Zeit)**
- 🔄 Aktualisiert sich **täglich automatisch** (2x täglich, stündlich während Spielen)

## 🔧 Setup (einmalig)

1. Kostenlosen API-Key holen bei [api-sports.io](https://api-sports.io)
2. Auf GitHub: **Settings → Secrets → Actions → New repository secret**
   - Name: `API_FOOTBALL_KEY`
   - Value: dein API-Key
3. Fertig! Der Kalender aktualisiert sich ab jetzt automatisch.

## 📁 Dateien

| Datei | Beschreibung |
|---|---|
| `WM2026.ics` | Der Kalender (wird automatisch aktualisiert) |
| `update_calendar.py` | Python-Skript das die Daten holt |
| `.github/workflows/update.yml` | GitHub Action (läuft automatisch) |
