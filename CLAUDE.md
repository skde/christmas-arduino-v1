# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Lantern Square: a 70 × 45 cm cardboard Christmas village with one Arduino Nano (ATmega168) and a PCA9685 board hidden in a 9 cm deep base under a removable deck. When the room goes dark, it runs a five-phase show: Dusk, Evening, Sleigh, Carol, Night.

The project is still in design. There is no firmware or build system yet. Layout:

- `README.md` (root): status, next steps and the file index. Update the status date and lines when a decision changes.
- `docs/01-concept.md` … `docs/06-turntable.md`: the design. The numbered files are the source of truth.
- `docs/05-open-questions.md`: open questions, plus a "Decided" list. Move items from open to decided rather than deleting them.
- `docs/inventory.txt`: the record of owned parts, written from photos that have since been removed. Treat this list as the record.
- `concept/concept-page.html`: the interactive concept page (Three.js 3D model, control box, wiring SVG, tables).
- `docs/07-houses.md`: house sizes, openings and materials. `tools/house-templates.py` generates the 1:1 templates in `drawings/templates/` (SVG pages, HTML, PDF). Keep its sizes in step with the `house()` calls in the concept page.
- `docs/08-tree.md`: the tree build. `tools/tree-templates.py` generates its templates in `drawings/templates/` and imports the page code from `house-templates.py`. Keep its tier sizes and pixel angles in step with `cR`, `cY` and the pixel loop in the concept page.
- `tools/turntable-section.py`: generates the turntable cross-section SVG `drawings/turntable-section.svg`.
- `firmware/`: not created yet; the firmware goes here.

This folder sits inside a larger git repo rooted at `/home/skde/Documents/test`. Don't commit unless asked.

## Hardware and firmware constraints that shape every change

- **ATmega168**: 1 KB RAM and about 14 KB of usable flash. Use Adafruit NeoPixel, not FastLED. Keep strings in `F()` and melodies in PROGMEM. The 16 × 16 matrix doesn't fit in RAM.
- **Pins and channels**: the pin plan and PCA9685 channel table are in `02-hardware.md`. Build on them instead of redesigning. Free PCA channels: 11, 14, 15. D3 is reserved for the IR receiver in the next version.
- **Pixel chains**:
  - D6 carries the 4 river pixels first (indices 0–3, steady blue), then the 30 string lights (indices 4–33).
  - D7 carries the 12 tree pixels through the slip ring.
  - Total pixel draw is capped in firmware at about 0.6 A.
- **One 5 V supply** shared by everything: the user's 5 V 5 A adapter with a 3 A fuse.
- When the pixel count, current draw or channel use changes, update the power table in `02-hardware.md` and in `concept-page.html` together.

## User preferences

- **Keep it simple.** Prefer fewer parts and less wiring. The design doesn't have to use every owned part. Offer extras as next-version items.
- **Basic parts.** Resistors, capacitors, diodes, transistors and the LDR are cheap to buy. Pick values and list them once. Don't raise them as open questions.
- **Static before moving.** New scenery starts static. Moving versions go to "Next version" unless the user asks for them. The gap behind the front ridge is taken by the sleigh arm.

## Concept page (`concept/concept-page.html`)

It's a single self-contained HTML file. Three.js r128 and OrbitControls come from a CDN, and all other JS sits in one inline `<script>`.

**Live artifact:** https://claude.ai/artifact/FHZcgud7m9V3Vm3JpK5WeD
- After editing, republish with the Artifact tool. Pass this `url` on the first publish in a session.
- If the publish is refused because the live version differs, compare the diff. If it only shows your own edits, publish the same file again.

**Keep the page in step with the markdown files:** elements table, pin table, wiring SVG, power and parts tables.

### Structure of the inline script

- `ch` holds channel state and mirrors what the firmware will hold. `SW` lists the checkbox ids (`c_<key>`), `PH` holds the show phases, and `applyPhase()` scripts each phase. A new light needs entries in `ch`, `SW`, `level`, `applyPhase`, `jump()` and the smoothing block in `frame()`.
- The scene has two groups:
  - `village` holds everything on the deck. It lifts by `DECK` (9) and up to 28 more when the user lifts the village.
  - `tray` holds the electronics in the base.
- See-through layer (`btnXray`): ghosts every village mesh except MeshBasic lights, `iceMat`, objects flagged `userData.keep`, and anything hanging below the deck. Parts made with `keep()` (LEDs in houses, bell servo, bakery floor) show only in see-through or lifted view. Tags with set `'xr'` show with the `'under'` tags.
- Optional wires layer (`ch.wires`, checkbox `c_wires`): red and black LED legs (`detailW`, replacing the grey `simpleW` stick), and one `plug()` per deck crossing with a `'wires'` tag. It shows only in the see-through or lifted view, and the plug list mirrors the "Deck plugs" table in `02-hardware.md`. While it is on, the `'xr'` LED tags are hidden.
- Helpers: `B()` box, `C()` cylinder, `M()` mesh, `paper()` material, `glow()` additive sprite, `addLight()`, `win()`, `house()`, `tag()` (3D labels: `'top'` shows on the deck, `'under'` shows when lifted), `wire()` and `riser()` (wiring shown when the village is lifted).

### Scene coordinates

Units are cm. The origin is the deck centre, x runs left to right and z runs back (−22.5) to front (+22.5). The deck surface in `village` is at y = 0.

| Item | Position |
|---|---|
| Backdrop | z = −22.25 |
| Back ridge | z = −20.5 |
| Front ridge | z = −15.5 |
| Sleigh servo pivot | (0, 3, −17) |
| Rink and turntable | centre (2, 3), disc radius 11, deck hole about 11.25 |
| River | curve `rvC` along the foot of the front ridge, about z −14.7 to −10.7 in the middle |
| Bridge | x = −6 |
| Sled run | x ≈ 2–11, on the front ridge face |
| Chapel | x = −23 |
| Bakery | x = 21.5 |
| Cottage | front left |
| Snowman | (22, 9) |

Keep new items clear of the rink hole and the river slot. About 2.5 cm of deck is all that's left between them.

### Previewing without a browser window

Render a screenshot with headless Chrome. The page loads Three.js from a CDN, so it needs internet access.

```bash
google-chrome --headless=new --disable-gpu --use-angle=swiftshader --enable-unsafe-swiftshader \
  --window-size=1400,1000 --virtual-time-budget=8000 --user-data-dir=<scratch>/chrome-N \
  --screenshot=<scratch>/shot.png "file://$PWD/concept/concept-page.html"
```

- Use a fresh `--user-data-dir` for each run, or later runs hang.
- Chrome may fail to load files from the scratchpad `/tmp` path. Copy a temp view file next to the page, render it, then delete it.
- For a close-up, render a temp copy with `cam.position.set(...)` / `orbit.target.set(...)` changed and labels off.
- Close-ups need smaller settings: `--window-size=900,700 --virtual-time-budget=3000`, wrapped in `timeout 120`. Chrome draws the scene on the CPU (swiftshader). Glow sprites that fill the screen near the camera make each frame slow, so the full-size settings hang past two minutes at close range. The smaller settings take about 75 s. The default view renders in about 20 s at full size.

Check the script's syntax by extracting the last `<script>` block and running `node --check` on it.

## Turntable drawing

```bash
python3 tools/turntable-section.py drawings/turntable-section.svg <inline-out.svg>
```

The first argument is the standalone SVG. The second is the inline version (`<svg class="tt" …>`), which must replace the matching block in `concept-page.html` by hand. Geometry is in cm from the axle (x) and the base floor (y). Heights depend on the slip ring, which still has to be measured when it arrives.
