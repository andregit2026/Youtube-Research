# YouTube-Recherche-Pipeline

Eine orchestrierte Pipeline, die: YouTube nach relevanten Videos durchsucht →
diese in NotebookLM lädt → KI-Analyse durchführt → optional ein Deliverable
erzeugt → einen vollständigen Markdown-Recherchebericht an den Nutzer zurückgibt.

---

## Was du vom Nutzer benötigst

Wenn dieser Workflow aufgerufen wird, extrahiere diese drei Angaben aus der
Nutzernachricht:

1. **Recherchethema** (erforderlich) — wonach auf YouTube gesucht werden soll
2. **Analyseziel** (erforderlich) — welche Frage beantwortet oder welcher Blickwinkel
   untersucht werden soll
3. **Deliverable-Typ** (optional) — falls nicht erwähnt, Deliverable-Schritt
   überspringen

Ist die Nutzernachricht bezüglich des Analyseziels unklar (z. B. nur "recherchiere
X"), stelle eine Klärungsfrage: *"Was möchtest du aus dieser Recherche konkret
verstehen oder mitnehmen?"*, bevor du weitermachst. Nicht nach Deliverables fragen —
wenn der Nutzer keins erwähnt hat, einfach ohne weitermachen.

### Zuordnung von Deliverable-Typen

Natürliche Sprache auf NotebookLM-Befehle abbilden:

| Nutzer sagt | NotebookLM-Befehl |
|-------------|-------------------|
| Karteikarten / flashcards | `generate flashcards --wait` |
| Quiz / Fragen | `generate quiz --wait` |
| Infografik | `generate infographic --wait` |
| Mindmap | `generate mind-map --wait` |
| Podcast / Audio | `generate audio --wait` |
| Folien / Präsentation | `generate slide-deck --wait` |
| Bericht / Briefing / Zusammenfassung | `generate report --format briefing-doc --wait` |
| Lernleitfaden | `generate report --format study-guide --wait` |
| Datentabelle | `generate data-table --wait` |

---

## Schritt-für-Schritt-Workflow

### Schritt 1 — YouTube-Suche

Das Skript `scripts/search_youtube.py` im `youtube-research` Skill mit Glob finden:

```bash
# Glob pattern
**/youtube-research/scripts/search_youtube.py
```

Mit `--count 10 --months 24` ausführen (breites Zeitfenster für gute Recherche-
abdeckung):

```bash
python <pfad-zum>/search_youtube.py "<recherchethema>" --count 10 --months 24
```

**Ausgabe vollständig erfassen** — sowohl lesbaren formatierten Text als auch
strukturierte Daten (URLs + Metadaten) für den Bericht benötigt. Jeden
Ergebnisblock parsen und extrahieren:
- Titel
- Kanalname + Abonnentenzahl
- Aufrufzahl
- Dauer
- Hochladedatum
- Engagement-Verhältnis
- URL

Falls weniger als 10 Ergebnisse zurückkommen, ist das in Ordnung — mit dem
Vorhandenen arbeiten. Falls 0 Ergebnisse, vor dem Aufgeben auf `--months 60`
erweitern.

### Schritt 1b — Videos filtern (immer vor dem Fortfahren anwenden)

**Alle Videos entfernen, deren Titel oder Kanal den folgenden Mustern entspricht,
bevor Quellen zu NotebookLM hinzugefügt oder in den Bericht aufgenommen werden:**

| Kategorie | Titel-/Kanal-Signale zum Ausschließen |
|-----------|---------------------------------------|
| Geldverdienen / Hustle | "make money", "earn money", "income", "$X/month", "$X/year", "how to get paid", "get rich", "passive income", "side hustle", "agency income", "freelance income", "monetize" |
| Dienstleistungsverkauf | "how to sell", "land clients", "get clients", "close deals", "sales funnel", "how I charge" |
| Kurs-/Coaching-Angebote | "my course", "join my", "enrol", "sign up for", "waitlist" |

Filter nach dem Parsen der yt-dlp-Ergebnisse in Python anwenden:

```python
EXCLUDE = [
    'make money', 'earn money', 'income', '/month', '/year',
    'how to get paid', 'get rich', 'passive income', 'side hustle',
    'agency income', 'freelance income', 'monetize',
    'land clients', 'get clients', 'close deals', 'sales funnel',
    'how i charge', 'my course', 'join my', 'enrol', 'waitlist',
]

def is_excluded(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in EXCLUDE)

videos = [v for v in videos if not is_excluded(v['title'])]
```

Titel aller gefilterten Videos protokollieren, damit der Nutzer sehen kann, was
aussortiert wurde. Das Ziel ist **ausschließlich Fachwissen und technische
Einblicke** — kein Business-/Hustle-Content.

### Schritt 2 — NotebookLM-Notizbuch erstellen (oder wiederverwenden)

Zuerst prüfen, ob für dieses Thema bereits ein Notizbuch vorhanden ist:

```bash
notebooklm list
```

Falls ein passendes Notizbuch gefunden wird, dieses wiederverwenden — **kein
Duplikat erstellen**:

```bash
notebooklm use <vorhandene_notizbuch_id>
```

Falls kein Notizbuch vorhanden ist, ein neues erstellen:

```bash
notebooklm create "<Recherchethema> - <Datumsbereich>"
notebooklm use <notizbuch_id>
```

Klar nach Thema und Datumsbereich benennen, damit es später leicht zu finden ist.

### Schritt 3 — YouTube-Quellen hinzufügen

Alle 10 Video-URLs als Quellen hinzufügen. YouTube-URLs werden von NotebookLM
automatisch erkannt. Mit `--wait` hinzufügen, damit jede indexiert ist, bevor
fortgefahren wird:

```bash
notebooklm source add <youtube_url>
```

Dies für alle 10 Videos durchführen. Falls eine Quelle nicht hinzugefügt werden
kann (Netzwerkfehler, privates Video), fehlgeschlagene protokollieren und
fortfahren — die gesamte Pipeline nicht abbrechen.

### Schritt 4 — Analyse durchführen

NotebookLM die Analysefrage des Nutzers stellen. **Immer `--json` verwenden**
(vermeidet Windows-cp1252-Emoji-Encoding-Absturz). Antwort vor dem Parsen
in eine Datei schreiben — das JSON kann 20 MB+ groß sein und überflutet das
Kontextfenster bei direkter Erfassung:

```bash
notebooklm ask "<analyseziel>" --json > Output/notebooklm_response.json
```

Antworttext dann mit Python extrahieren:

```python
import json, sys
with open("Output/notebooklm_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)
answer = data.get("answer") or data.get("text") or str(data)
print(answer[:5000])  # Vorschau
```

Auch als Notiz zur späteren Referenz speichern:

```bash
notebooklm ask "<analyseziel>" --save-as-note --note-title "Recherche-Analyse" --json
```

**Windows-Emoji-Encoding-Workaround:** Falls ein `notebooklm`-Befehl (z. B.
`source list`) mit `UnicodeEncodeError` abstürzt, immer `--json` hinzufügen und
Ausgabe via Python's `sys.stdin.buffer.read().decode('utf-8')` parsen oder stdout
mit `> output.json` in Datei schreiben und explizit mit `encoding="utf-8"` einlesen.

### Schritt 5 — Deliverable generieren (falls angefordert)

Falls der Nutzer ein Deliverable angefordert hat, dieses generieren und
herunterladen:

```bash
notebooklm generate <befehl> --wait
notebooklm download <typ> ./<thema-slug>-<deliverable-typ>.<erweiterung>
```

Sauberen Dateinamen-Slug verwenden: Kleinbuchstaben, Leerzeichen durch Bindestriche
ersetzen, keine Sonderzeichen.
Beispiel: `ki-agenten-2025-karteikarten.md` oder `quantencomputing-quiz.json`.

### Schritt 6 — Recherchebericht zusammenstellen

Einen Markdown-Bericht in `Output/<thema-slug>-recherchebericht.md` schreiben.
Eine Zusammenfassung direkt im Chat ausgeben (nicht das vollständige Markdown
ausgeben — zu lang).

### Schritt 7 — HTML-Bericht generieren

Immer eine HTML-Version erstellen. **In `Output/JJJJMMTT_<thema-slug>.html`
speichern** (JJJJMMTT-Präfix sorgt für korrekte Sortierung nach Datum). Dann öffnen:

```bash
start Output/JJJJMMTT_<thema-slug>.html   # Windows
```

HTML über ein Python-Skript (`Output/gen_<thema-slug>.py`) generieren statt
rohes HTML inline schreiben — so bleibt der Generator wiederverwendbar und
vermeidet Editor-Grenzen.

CSS/HTML-Vorlagen, Farbpalette, Toggle-JavaScript und Seitenstruktur befinden
sich in `references/html-design-system.md` — diese Datei lesen, bevor der
HTML-Bericht generiert wird.

---

## Berichtsformat

Diese genaue Vorlage verwenden (alle Platzhalter ausfüllen):

```markdown
# Recherchebericht: <Recherchethema>

**Datum:** <heutiges Datum>
**Analyseziel:** <vom Nutzer angegebenes Analyseziel>
**NotebookLM-Notizbuch:** <notizbuch_id>

---

## YouTube-Quellen

> 10 Videos gefunden via yt-dlp-Suche: "<abfrage>" | Letzte 24 Monate

| # | Titel | Kanal | Aufrufe | Dauer | Hochgeladen | Engagement | URL |
|---|-------|-------|---------|-------|-------------|------------|-----|
| 1 | <titel> | <kanal> (<abonnenten>) | <aufrufe> | <dauer> | <datum> | <verhältnis>x | [Link](<url>) |
...

### Quellendetails

Für jedes Video einen kurzen Eintrag einfügen:
**#01 - <Titel>**
- Kanal: <name> | <abonnenten> Abonnenten
- Aufrufe: <aufrufe> | Dauer: <dauer> | Hochgeladen: <datum>
- Engagement: <verhältnis>x
- URL: <url>

---

## Analyse

> Frage: <analyseziel>

<Vollständige Antwort von NotebookLM, einschließlich Quellenverweise>

---

## Deliverable

> Typ: <deliverable-typ> — gespeichert unter `./<dateiname>`

<Falls kein Deliverable angefordert wurde, diesen Abschnitt vollständig weglassen>

---

## Suchmetadaten

| Feld | Wert |
|------|------|
| Suchanfrage | <verwendete Abfrage> |
| Tool | yt-dlp |
| Angeforderte Ergebnisse | 10 |
| Abgerufene Ergebnisse | <N> |
| Zeitfenster | Letzte 24 Monate |
| Suchdatum | <heute> |
| Erfolgreich zu NotebookLM hinzugefügte Quellen | <N von 10> |
| NotebookLM-Notizbuch-ID | <id> |
| Deliverable generiert | <Ja / Nein> |
```

---

## Fehlerbehandlung

- **yt-dlp nicht installiert**: `pip install yt-dlp` vor dem Suchschritt ausführen
- **yt-dlp Timeout** (standardmäßig 120s): Eine zielgerichtete JSON-Datei statt
  Live-Suche verwenden — `yt-dlp ytsearch1:"<exakter Videotitel>" --dump-json --quiet`
  pro Video ausführen, oder `--count` reduzieren und `--months` erhöhen
- **NotebookLM nicht authentifiziert**: `notebooklm login` ausführen und den Nutzer
  bitten, den Browser-Login abzuschließen, dann fortfahren
- **Quelle hinzufügen fehlgeschlagen**: Dieses Video überspringen, in den
  "Suchmetadaten" unter der Zeile "Fehlgeschlagene Quellen" vermerken
- **Analyse liefert leeres Ergebnis**: Einmal mit leicht umformuliertem Analyseziel
  wiederholen
- **Windows cp1252 UnicodeEncodeError** (z. B. `notebooklm source list` stürzt bei
  Emojis in Videotiteln wie 🎬 ab): Immer `--json` zu jedem `notebooklm`-Befehl
  hinzufügen, der Titel oder Beschreibungen ausgibt. Stdout in Datei schreiben
  (`> out.json`) und mit Python `open(..., encoding="utf-8")` einlesen
- **NotebookLM-JSON-Antwort zu groß für den Kontext** (20 MB+): Mit
  `> response.json` in Datei schreiben, mit Python parsen, nur die ersten 5000
  Zeichen im Chat anzeigen
- **Python SyntaxError im HTML-Generator** — JS `{`/`}` innerhalb von `f"""..."""`:
  Alle `<script>`-Blöcke in einen einfachen `"""` String auslagern
  (`JS_BLOCK = """<script>...</script>"""`), als `{JS_BLOCK}` im f-String
  referenzieren — niemals rohes JS in einen f-String einbetten

---

## Tipps für gute Ergebnisse

- **Inhaltsfilter ist Pflicht** — den Filter aus Schritt 1b immer anwenden, bevor
  Quellen zu NotebookLM hinzugefügt oder der Bericht erstellt wird. Das Ziel ist
  Fachwissen und technische Einblicke; Geldverdienen-, Hustle- und
  Kurs-Upsell-Videos werden unabhängig von Aufrufzahl oder Engagement-Verhältnis
  nie aufgenommen.
- Das Recherchethema des Nutzers wörtlich als Suchanfrage verwenden; nur
  offensichtlich problematische Zeichen bereinigen (Anführungszeichen, Schrägstriche)
- Beim Stellen der NotebookLM-Analysefrage so formulieren, dass der Videoinhalt
  genutzt wird: "Basierend auf den YouTube-Videos in diesem Notizbuch, <analyseziel>"
- Das Engagement-Verhältnis in der YouTube-Ausgabe ist ein Signal — Videos über
  1,0x enthalten oft Informationen, die über das bestehende Publikum des Kanals
  hinaus verbreitet wurden, was auf besonders wertvolle oder neue Inhalte hinweisen kann
- **Zielgerichtete URL-Suche** — falls bereits eine Titelliste vorhanden ist (z. B.
  aus einer gespeicherten `yt_targeted.json`) und nur die kanonische YouTube-URL
  für jedes Video benötigt wird:
  ```bash
  yt-dlp ytsearch1:"<exakter Titel>" --dump-json --quiet --no-playlist
  ```
  `.webpage_url` aus der JSON-Ausgabe parsen. Viel schneller als eine breite Suche.
- **HTML aus einem Python-Skript generieren, nicht inline** — für Berichte mit 20+
  Videos `Output/gen_<thema>.py` schreiben, das alle Videodaten und die HTML-Vorlage
  enthält, dann ausführen, um das finale `.html` zu erzeugen. Dies macht die
  Generierung reproduzierbar und vermeidet Kontextfenster-Grenzen beim direkten
  Schreiben großer HTML-Dateien.
