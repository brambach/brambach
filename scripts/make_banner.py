import base64, random, pathlib
F = pathlib.Path(__file__).resolve().parent / "fonts"  # copy the Instrument Serif and JetBrains Mono woff2 files here
def b64(name): return base64.b64encode((F/name).read_bytes()).decode()
SERIF, MONO = b64("InstrumentSerif-latin.woff2"), b64("JetBrainsMono-latin-400.woff2")

THEMES = {
  "light": dict(paper="#f7f6f3", line="#ebeae5", ink="#1b1b19", muted="#6d6c66", empty="#ebeae5",
                green=["#cfe3d3", "#8fc19c", "#4f9a63", "#2f7844"]),
  "dark":  dict(paper="#171716", line="#2d2d2b", ink="#ecece9", muted="#9b9a93", empty="#252523",
                green=["#1f3326", "#2f5a3b", "#4f9463", "#7cc58f"]),
}
W, H = 1200, 320
COLS, ROWS, CELL, GAP = 18, 7, 16, 5
GX = W - 72 - (COLS*(CELL+GAP)-GAP)
GY = 172 - (ROWS*(CELL+GAP)-GAP) // 2

def grid(t):
    rnd = random.Random(23)  # fixed seed, same pattern in both themes
    out = []
    for c in range(COLS):
        fade = min(1, (c + 1) / 5)  # leftmost columns fade in
        density = 0.25 + 0.7 * (c / (COLS - 1))  # busier toward today
        for r in range(ROWS):
            if c == COLS - 1 and r > 2: continue  # this week isn't over yet
            lvl = 0
            if rnd.random() < density:
                lvl = min(4, 1 + int(rnd.random() * (1 + 3 * c / (COLS - 1)) + 0.4))
            fill = t["empty"] if lvl == 0 else t["green"][lvl - 1]
            x, y = GX + c*(CELL+GAP), GY + r*(CELL+GAP)
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3.5" fill="{fill}" opacity="{fade:.2f}"/>')
    return "\n    ".join(out)

for name, t in THEMES.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Bryce Rambach. San Diego, building Dervo.">
  <style>
    @font-face {{ font-family: "IS"; src: url(data:font/woff2;base64,{SERIF}) format("woff2"); }}
    @font-face {{ font-family: "JM"; src: url(data:font/woff2;base64,{MONO}) format("woff2"); }}
    .name {{ font-family: "IS", Georgia, serif; font-size: 108px; letter-spacing: -1.5px; fill: {t["ink"]}; }}
    .eyebrow {{ font-family: "JM", ui-monospace, Menlo, monospace; font-size: 17px; letter-spacing: 2.6px; fill: {t["muted"]}; }}
  </style>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="{t["paper"]}" stroke="{t["line"]}"/>
  <text class="eyebrow" x="76" y="118">SAN DIEGO, CA</text>
  <text class="name" x="70" y="210">Bryce Rambach</text>
  <text class="eyebrow" x="76" y="256">BUILDING DERVO</text>
  <g>
    {grid(t)}
  </g>
</svg>
'''
    pathlib.Path(__file__).resolve().parent.parent / f"assets/banner-{name}.svg".write_text(svg)
    print(name, len(svg)//1024, "KB")
