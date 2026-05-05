# YouTube-Suche

YouTube mit `yt-dlp` durchsuchen und strukturierte Ergebnisse mit umfangreichen
Metadaten und einer Engagement-Metrik zurückgeben — übersichtlich formatiert.

---

## Voraussetzungen

Prüfen, ob `yt-dlp` installiert ist:

```bash
yt-dlp --version
```

Falls nicht vorhanden, installieren:

```bash
pip install yt-dlp
```

---

## Das Suchskript

Das gebündelte Skript liegt unter `scripts/search_youtube.py` (relativ zum
`youtube-research` Skill-Verzeichnis). Pfad mit Glob finden:

```bash
# Glob pattern
**/youtube-research/scripts/search_youtube.py
```

Ausführen über die Kommandozeile:

```bash
python scripts/search_youtube.py "Suchanfrage" [Optionen]
```

| Flag | Standard | Beschreibung |
|------|----------|--------------|
| `--count` | 20 | Anzahl der zurückzugebenden Ergebnisse |
| `--months` | 6 | Nur Videos der letzten N Monate anzeigen |

**Beispiele:**

```bash
# Top-20-Ergebnisse der letzten 6 Monate (Standard)
python scripts/search_youtube.py "Rust-Programmier-Tutorial"

# Top-10-Ergebnisse, letzte 3 Monate
python scripts/search_youtube.py "KI-Agenten 2025" --count 10 --months 3

# 30 Ergebnisse, kein Zeitfilter (Monate hoch setzen)
python scripts/search_youtube.py "Pasta kochen" --count 30 --months 120
```

---

## Wie die Ausgabe aussieht

Jedes Ergebnis ist durch eine horizontale Trennlinie getrennt:

```
YouTube Search Results: 'python tutorial'
Last 6 months  |  Showing 20 result(s)
────────────────────────────────────────────────────────────────────────────────
#01  Python for Beginners – Full Course
      Channel:    Tech With Tim  (1.2M subscribers)
      Views:      890.5K   Duration: 1:42:15   Uploaded: Nov 03, 2025
      Engagement: 0.74x (views / subscribers)
      URL:        https://www.youtube.com/watch?v=...
--------------------------------------------------------------------------------
```

**Engagement-Verhältnis** = `Aufrufe / Abonnenten`.
- Werte **über 1,0x**: Das Video hat mehr Aufrufe erzielt als der Kanal Abonnenten hat —
  starkes Signal für Empfehlungsleistung oder virale Reichweite.
- Werte **unter 0,1x**: Das Video hat im Vergleich zur Kanalzielgruppe schwach abgeschnitten.
- `N/A`: Abonnentenzahl war nicht verfügbar.

---

## Arbeitsablauf

Wenn ein Nutzer nach YouTube-Videos suchen möchte, diese Schritte ausführen:

1. **Suchanfrage** und etwaige Einschränkungen (Zeitfenster, Ergebnisanzahl) aus der
   Nutzernachricht extrahieren.
2. Pfad zu `search_youtube.py` auflösen — liegt unter `scripts/search_youtube.py`
   im `youtube-research` Skill-Verzeichnis.
3. Prüfen, ob `yt-dlp` verfügbar ist (`yt-dlp --version`); bei Bedarf installieren.
4. Skript mit den passenden Argumenten ausführen.
5. Ausgabe direkt an den Nutzer weitergeben — das Skript formatiert sie bereits übersichtlich.
6. Folgeaktionen anbieten:
   - Nach Engagement, Aufrufen oder Abonnentenzahl sortieren (Rohdaten in Python nachverarbeiten).
   - Auf einen bestimmten Kanal filtern.
   - Einzelnes Video detaillierter abrufen mit `yt-dlp --dump-json <url>`.

---

## Sonderfälle

- **Keine Ergebnisse**: Zeitfenster erweitern (`--months 24`) oder Suchanfrage vereinfachen.
- **Abonnentenzahl N/A**: YouTube gibt für kleine oder halbprivate Kanäle manchmal keine
  Abonnentendaten aus; das Engagement-Verhältnis ist dann `N/A`.
- **Langsam / Timeout**: yt-dlp kann bei vielen Ergebnissen langsam sein. Falls
  `--count 20` + `--months 6` zu Timeouts führt, `--count` reduzieren oder `--months`
  erhöhen, um den internen Multiplikator zu senken.
- **Rate-Limiting**: Falls yt-dlp Fehler wegen Rate-Limits oder Bot-Erkennung meldet,
  einige Minuten warten und erneut versuchen. Nicht in einer engen Schleife scrapen.

---

## Ausgabedateien

Berichte, Analysen und Zusammenfassungen immer als zwei Dateien in `Output/` speichern —
`JJJJMMTT_<thema-slug>.md` und `JJJJMMTT_<thema-slug>.html`.
HTML niemals weglassen. Dateibenennungskonvention, Farbpalette und vollständige
HTML-Vorlage: `references/html-design-system.md` im `youtube-research` Skill.

---

## Sortierung und Nachverarbeitung

Falls der Nutzer eine andere Rangfolge möchte (z. B. nach Engagement statt nach
YouTube-Relevanz), das Skript mit einem höheren `--count` ausführen und dann in Python
sortieren:

```python
import json, subprocess

result = subprocess.run(
    ["yt-dlp", "ytsearch50:Suchanfrage", "--dump-json", "--quiet"],
    capture_output=True, text=True
)
videos = [json.loads(l) for l in result.stdout.strip().split("\n") if l]
videos.sort(key=lambda v: (v.get("view_count") or 0) / max(v.get("channel_follower_count") or 1, 1), reverse=True)
```
