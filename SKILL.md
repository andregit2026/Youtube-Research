---
name: youtube-research
description: >
  Vollautomatisierte YouTube-Recherche-Pipeline, die YouTube-Suche, KI-gestützte
  Tiefenanalyse via NotebookLM und formatierte HTML-Berichte kombiniert.
  Diesen Skill verwenden, wenn der Nutzer YouTube durchsuchen, Videos zu einem
  Thema finden und analysieren, eine Wissensdatenbank aus YouTube-Inhalten
  aufbauen, strukturierte Rechercheergebnisse mit Engagement-Metriken erhalten
  oder ein Deliverable (Karteikarten, Quiz, Infografik, Podcast, Folien)
  aus YouTube-Videos generieren möchte.
  Auslösen, wenn der Nutzer sagt: "Suche auf YouTube nach X",
  "Recherchiere [Thema] mit YouTube", "Finde und analysiere YouTube-Videos über Y",
  "Was schauen die Leute auf YouTube über Z", "YouTube-Recherche zu [Thema]",
  "Erstelle einen Bericht über YouTube-Videos zu X" oder ähnliches.
  Auch auslösen, wenn yt-dlp, NotebookLM oder YouTube-Analyse erwähnt werden.
compatibility:
  tools: [Bash, Glob, Write]
  dependencies: [yt-dlp, notebooklm-py, playwright]
---

# YouTube-Recherche

```
youtube-search  ──►  youtube-research-pipeline  ──►  notebooklm
  (Videos finden)       (Pipeline orchestrieren)      (KI-Analyse + Output)
```

## Welche Referenz lesen?

Basierend auf der Nutzeranfrage die passende Referenzdatei lesen — nicht alle
auf einmal, nur die benötigte:

| Nutzer möchte ... | Referenz lesen |
|---|---|
| Nur YouTube-Videos finden und Metadaten sehen | `references/youtube-search.md` |
| Vollständige Recherche: Suche + Analyse + HTML-Bericht | `references/youtube-research-pipeline.md` |
| HTML-Bericht generieren (CSS, Layout, Toggle-JS) | `references/html-design-system.md` |
| NotebookLM direkt steuern (Podcasts, Quizze, Folien...) | `references/notebooklm.md` lesen |

Das Such-Skript liegt unter `scripts/search_youtube.py` — kein separates Verzeichnis
nötig, Glob-Suche nach `**/youtube-research/scripts/search_youtube.py`.

---

## Voraussetzungen

```bash
pip install yt-dlp
pip install notebooklm-py "notebooklm-py[browser]"
playwright install chromium
notebooklm login   # einmalig, öffnet Browser
```

---

## Ausgabe

Alle Dateien in `Output/` speichern:

| Datei | Inhalt |
|---|---|
| `JJJJMMTT_<thema>.html` | Gestalteter HTML-Bericht (eigenständig, dunkles Theme) |
| `gen_<thema>.py` | Python-Generator des HTML-Berichts (wiederverwendbar) |
| `yt_<thema>.json` | Rohe yt-dlp-Suchergebnisse |
| `notebooklm_response.json` | Rohe NotebookLM-Analyse |

---

## Häufige Probleme

- **yt-dlp keine Ergebnisse**: `--months 24` oder `--count` reduzieren
- **NotebookLM nicht authentifiziert**: `notebooklm login` erneut ausführen
- **UnicodeEncodeError (Windows)**: Immer `--json` + `> output.json` + `open(..., encoding="utf-8")`
- **JSON-Antwort zu groß**: `> response.json` schreiben, mit Python parsen
