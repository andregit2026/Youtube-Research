# HTML-Bericht-Design-System (Produktionserprobt)

## Dateibenennungskonvention
- **Immer `JJJJMMTT_<thema-slug>.html`** im Ordner `Output/` verwenden.
  Beispiel: `20260424_claude_code_youtube_analyse.html`
- Zusammen mit `Output/gen_<thema-slug>.py` speichern, damit der Bericht
  neu generiert werden kann.

## Seitenstruktur (von oben nach unten)
1. Sticky obere Navigationsleiste (nur Titel — keine Tabs)
2. Header-Block (Titel + Datumsbereich + Meta-Pills + **Abschnitt-Sprung-Panel**)
3. Statistik-Leiste
4. **Ranglistentabelle** (mit Rangfolge-Hinweis + aufklappbaren Schlüsselpunkt-Zeilen)
5. Features-Abschnitt (`id="features"`)
6. Lücken-Abschnitt (`id="gaps"`)
7. Footer

## Dunkles Farbschema
```css
--bg:    #0d1117;   /* Seitenhintergrund */
--card:  #111827;   /* Abschnittskarten */
--card2: #1a2233;   /* Tabellenzeile / Button-Hintergrund */
--border:#2d3748;
--text:  #e2e8f0;
--muted: #94a3b8;
--accent:#818cf8;   /* Indigo — primärer Akzent */
```

## Sticky obere Navigationsleiste (nur Titel — keine Tab-Buttons)

Die Topnav ist eine schmale Frosted-Glass-Leiste, die nur den Berichtstitel
zeigt. Die Abschnittsnavigation befindet sich im Header (siehe unten), so dass
sie immer sichtbar ist, ohne dauerhaft Bildschirmfläche zu beanspruchen.

```html
<div class="topnav">
  <span class="topnav-title">Thema <span>Datumsbereich</span></span>
</div>
```

```css
.topnav {
  position:sticky; top:0; z-index:100;
  background:rgba(13,17,23,.92); backdrop-filter:blur(12px);
  border-bottom:1px solid var(--border);
  padding:9px 40px;
  display:flex; align-items:center; gap:10px;
}
.topnav-title { font-size:13px; font-weight:700; color:#fff; white-space:nowrap; }
.topnav-title span { color:var(--muted); font-weight:400; font-size:11px; margin-left:6px; }
main { padding:28px 40px; max-width:1200px; margin:0 auto; }
```

## Abschnitt-Sprung-Panel (im Header, nach den Pills)

Ein "↓ Zum Abschnitt springen"-Label + 3 breite Karten-Buttons direkt nach dem
Pills-Streifen im `<header>` platzieren. Jeder Button hat ein großes Icon,
fetten Titel und eine kurze Hinweiszeile. Deutlich klickbar (Hover hebt an +
Indigo-Glühen).

```html
<p class="snav-label">&#8595; Zum Abschnitt springen</p>
<div class="section-nav">
  <a class="snav-btn" href="#overview">
    <span class="snav-icon">&#9733;</span>
    <span class="snav-text">
      <span class="snav-title">Übersicht &amp; Rangliste</span>
      <span class="snav-hint">Alle N Videos mit Schlüsselpunkten</span>
    </span>
  </a>
  <a class="snav-btn" href="#features">
    <span class="snav-icon">&#10022;</span>
    <span class="snav-text">
      <span class="snav-title">Neueste Features</span>
      <span class="snav-hint">Was diese Woche neu ist</span>
    </span>
  </a>
  <a class="snav-btn" href="#gaps">
    <span class="snav-icon">&#9651;</span>
    <span class="snav-text">
      <span class="snav-title">Lücken in der Abdeckung</span>
      <span class="snav-hint">Themen, die noch niemand behandelt</span>
    </span>
  </a>
</div>
```

```css
.snav-label { font-size:10.5px; text-transform:uppercase; letter-spacing:.09em;
              color:var(--muted); font-weight:600; margin-top:18px; margin-bottom:8px; }
.section-nav { display:flex; gap:10px; flex-wrap:wrap; }
.snav-btn {
  display:inline-flex; align-items:center; gap:12px;
  padding:11px 18px; border-radius:10px; flex:1; min-width:160px;
  background:rgba(255,255,255,.055); border:1px solid rgba(255,255,255,.13);
  color:#e2e8f0; text-decoration:none;
  transition:background .18s, border-color .18s, transform .12s, box-shadow .18s;
  cursor:pointer;
}
.snav-btn:hover {
  background:rgba(124,106,247,.2); border-color:#818cf8; color:#c4b5fd;
  transform:translateY(-1px); box-shadow:0 4px 16px rgba(99,102,241,.18);
}
.snav-icon  { font-size:20px; flex-shrink:0; line-height:1; }
.snav-text  { display:flex; flex-direction:column; gap:2px; }
.snav-title { font-size:13px; font-weight:700; line-height:1.2; }
.snav-hint  { font-size:10.5px; color:var(--muted); line-height:1.3; }
```

## Rangfolge-Hinweis (unterhalb der Ranglistentabellen-Überschrift)

Immer eine kurze Infobox direkt nach dem `<div class="shdr">` für die
Ranglistentabelle einfügen, die erklärt, dass die Rangfolge nach
**Inhaltstiefe** und nicht nach Aufrufzahl erfolgt. Ein konkretes Beispiel
nennen, damit Nutzer der Methodik vertrauen.

```html
<div class="rank-note">
  <span class="rank-note-icon">&#9432;</span>
  <p>
    <b>Wie Videos eingestuft werden:</b> Die Rangfolge spiegelt <b>Inhaltstiefe
    und Qualität der Erkenntnisse</b> wider, nicht die rohe Aufrufzahl. Faktoren
    umfassen einzigartige demonstrierte Techniken, praktische Erkenntnisse pro
    Minute, Signal-Rausch-Verhältnis und ob das Video etwas abdeckt, das in
    dieser Woche nirgendwo sonst zu finden ist. Ein Video mit vielen Aufrufen
    und dünnem Inhalt steht niedriger &mdash; zum Beispiel ist
    <em>&ldquo;[Titel]&rdquo;</em> das meistgesehene Video der Woche, läuft aber
    nur N Minuten (davon ~1 Min. Werbung) und behandelt das Thema oberflächlich,
    weshalb es trotz seiner Aufrufzahl außerhalb der Top {n} liegt.
    Auf eine beliebige Zeile klicken, um die Schlüsselpunkte aufzuklappen und
    selbst zu urteilen.
  </p>
</div>
```

```css
.rank-note { background:rgba(245,158,11,.06); border:1px solid rgba(245,158,11,.22);
             border-radius:9px; padding:12px 16px; margin-bottom:18px;
             display:flex; gap:12px; align-items:flex-start; }
.rank-note-icon { font-size:16px; flex-shrink:0; margin-top:1px; line-height:1; }
.rank-note p    { font-size:12px; color:#cbd5e1; line-height:1.65; margin:0; }
.rank-note p b  { color:#fbbf24; }
.rank-note p em { color:var(--muted); font-style:normal; }
```

## Ranglistentabelle mit aufklappbaren Schlüsselpunkten

Jedes Video belegt **zwei** `<tr>`-Zeilen: die sichtbare Video-Zeile und eine
versteckte Schlüsselpunkte-Zeile. Klick auf die Video-Zeile (oder ihren
Expand-Button) wechselt die zweite Zeile.

**Video-Zeile (`vrow`)**:
```html
<tr id="v{rang}" class="vrow" onclick="toggleKP('kp{rang}')">
  <td class="rank-cell">
    <div class="rank-btn" id="ico{rang}">
      <span class="rn">{rang}</span>
      <span class="rlabel">aufklappen</span>
      <span class="rc">&#8964;</span>
    </div>
  </td>
  <td class="title-cell"><a href="{url}" target="_blank">{titel}</a>
    <div class="ch">{kanal}</div></td>
  <td>{aufrufe}</td><td>{likes}</td><td>{dauer}</td>
  <td class="date-cell">{datum}</td>
  <td><span class="badge" style="background:{sig_bg};color:{sig_fg};">{sig_label}</span></td>
</tr>
```

**Schlüsselpunkte-Zeile (`kprow`)** — startet ausgeblendet, umspannt alle Spalten:
```html
<tr id="kp{rang}" class="kprow" style="display:none;">
  <td colspan="7" class="kp-td" style="border-left:4px solid {akzent_farbe};">
    <div class="kp-inner">
      <div class="kp-thumb">
        <img src="https://img.youtube.com/vi/{vid_id}/mqdefault.jpg" loading="lazy">
        <a class="wb" href="{url}" target="_blank">Ansehen</a>
      </div>
      <div class="kp-right">
        <div class="kph" style="color:{akzent_farbe};">Schlüsselpunkte aus dem Transkript</div>
        <ul class="kplist" style="--dot:{akzent_farbe};">
          <li>Punkt eins</li>
          <li>Punkt zwei</li>
          ...
        </ul>
      </div>
    </div>
  </td>
</tr>
```

## Expand-Button-CSS (immer sichtbar — nicht nur beim Hover)
```css
.rank-btn {
  display:inline-flex; flex-direction:column; align-items:center;
  width:46px; border-radius:10px; padding:7px 4px 6px; gap:1px;
  background:var(--card2); border:1.5px solid #4a5568;   /* immer sichtbar */
  cursor:pointer; user-select:none;
  transition:background .18s, border-color .18s, box-shadow .18s;
}
.rank-btn:hover { background:#312e81; border-color:#6366f1;
                  box-shadow:0 0 0 3px rgba(99,102,241,.25); }
.rank-btn .rn    { font-weight:800; font-size:1rem; color:#e2e8f0; line-height:1; }
.rank-btn .rlabel{ font-size:9px; font-weight:600; text-transform:uppercase;
                   letter-spacing:.07em; color:#818cf8; }
.rank-btn .rc    { font-size:12px; color:#818cf8; transition:transform .25s; line-height:1; }
.rank-btn.open   { background:#4f46e5; border-color:#6366f1; }
.rank-btn.open .rn     { color:#fff; }
.rank-btn.open .rlabel { color:#c4b5fd; }
.rank-btn.open .rc     { color:#fff; transform:rotate(180deg); }

.kp-inner { display:flex; gap:18px; padding:4px 0; }
.kp-thumb img { width:160px; border-radius:8px; display:block; }
.wb { display:block; text-align:center; margin-top:8px; font-size:12px;
      background:#4f46e5; color:#fff; padding:5px; border-radius:6px; text-decoration:none; }
.kph { font-weight:700; font-size:13px; margin-bottom:10px; }
.kplist { margin:0; padding-left:0; list-style:none; display:flex; flex-direction:column; gap:7px; }
.kplist li { font-size:12.5px; color:#cbd5e1; line-height:1.5; padding-left:18px;
             position:relative; }
.kplist li::before { content:"•"; position:absolute; left:0; color:var(--dot); font-size:14px; }
```

## Toggle-JavaScript (einfacher String — KEIN f-String)
JS muss in einem **einfachen** `"""` String stehen, niemals in einem `f"""` String.
Pythons f-Strings interpretieren `{` und `}` als Ausdrücke, was JS-Funktionsrümpfe
bricht.

```python
JS_BLOCK = """<script>
function toggleKP(id) {
  var row  = document.getElementById(id);
  var rank = id.replace('kp','');
  var btn  = document.getElementById('ico' + rank);
  var open = row.style.display !== 'none';
  row.style.display = open ? 'none' : '';
  if (btn) {
    btn.classList.toggle('open', !open);
    var lbl = btn.querySelector('.rlabel');
    if (lbl) lbl.textContent = open ? 'aufklappen' : 'zuklappen';
  }
}
</script>"""

HTML = f"""<!DOCTYPE html>...{JS_BLOCK}</body></html>"""
```

## Abschnitts-Farbpalette (eine je Video/Thema, zyklisch)
| Slot | Farbe | Hex |
|------|-------|-----|
| 1 | Indigo | `#818cf8` |
| 2 | Bernstein | `#f59e0b` |
| 3 | Smaragd | `#34d399` |
| 4 | Rot | `#f87171` |
| 5 | Lila | `#c084fc` |
| 6 | Cyan | `#67e8f9` |
| 7 | Rosa | `#fb7185` |
| 8+ | wiederholen | ab Slot 1 |

## Meta-Pills-Streifen (Header)
```html
<div class="meta-pills">
  <span class="pill">&#128198; {datum}</span>
  <span class="pill">&#127909; {n} Videos</span>
  <span class="pill">&#128221; NotebookLM: {notizbuch_id}</span>
</div>
```

## Footer
```html
<footer>Erstellt von youtube-research Skill &mdash; Claude Code &mdash; {datum}</footer>
```

## Allgemeine Regeln
- Vollständig eigenständig — keine externen CSS- oder JS-Abhängigkeiten
- Alle externen Links mit `target="_blank"` öffnen
- YouTube-Vorschaubilder via `https://img.youtube.com/vi/{vid_id}/mqdefault.jpg`
- `loading="lazy"` bei allen Vorschaubild-`<img>`-Tags verwenden
- **Video-Anzahl immer dynamisch**: `{len(VIDEOS)}` im f-String verwenden — niemals eine Zahl hardcoden. Das gilt für Meta-Pills, rank-note, Features-Abschnitt und alle anderen Stellen im HTML, die die Gesamtzahl der Videos nennen.
