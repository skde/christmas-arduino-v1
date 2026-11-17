# Houses: sizes and templates

Status: drafted 2026-11-17. Sizes match the 3D model in `concept/concept-page.html`.

Printable 1:1 templates: `drawings/templates/house-templates.pdf` (15 A4 pages: chapel 1–7, bakery 8–12, cottage 13–15). Print at 100 %, then check the 5 cm bar on each page. To regenerate after a change, run `python3 tools/house-templates.py`, then print `drawings/templates/house-templates.html` to PDF.

## Materials and joints

Corrugated is much cheaper, so it's used everywhere except the walls that have windows.

| Material | Pieces |
|---|---|
| Bookbinding board, 1.5 mm | Walls with windows: chapel right side wall, tower front, 2 tower sides, bakery front gable, cottage front gable. 4 A5 sheets |
| Corrugated, single-wall 3 mm | Everything else: back gables, plain side walls, roofs, chapel gables, tower back, divider, shelf, top plate, bakery floor and supports. Well under one 1200 × 800 sheet |
| Thin card (cereal box) | Spire, chimneys, hearth box |
| Thin card (cereal box) | Awning, so it does not droop over the shop window |

- Board pieces don't fold. Each wall and roof panel is a separate piece, glued edge to edge. Fold lines appear only on the thin-card pieces.
- Butt joints: the gable walls are full width, and the side walls fit between them. Each side wall is therefore shorter than the house depth by the thickness of the two gables it sits between, for example 1.5 + 3 mm when the front is board and the back is corrugated. The templates already include this. To change a thickness, set `TB` or `TC` in the script and rerun it.
- Corrugated: cut walls with the flutes running upright, which makes them stiffer and stops them bowing. Flutes on the roof run down the slope. Use a sharp blade and a steel rule, and make two or three light passes. Cover exposed flute edges with a paper strip, paint or snow.
- Joining board to corrugated: PVA or hot glue. Add a strip of tape along each inside corner to stop light leaks.
- Window bars: leave 2 mm bars in the board. If they break, cut the whole opening and glue thin card strips on afterwards. Glue tracing paper behind the window (tissue for the chapel).
- Inside: line with white paper or foil for an even glow. There is no floor. Each house sits over a 1 cm hole in the deck for its LED leads. Two places need their own extra hole: the chapel tower (blue LED and bell servo, closed off from the nave) and the cottage hearth box (flicker LEDs). Mark the holes from the built houses, not from the 3D model: the built tower stands 0.8 cm further forward.
- Roof: two corrugated panels per house. Panel B is 3 mm wider so it overlaps A at the ridge. Overhang is 0.5 cm at the eaves and 0.8 cm at each gable end, except the chapel front, which ends flush so the tower can stand against the gable. Snow (cotton or white paper) covers the ridge.

## Sizes (cm)

Width is across the front, depth is front to back, and wall height is to the eaves.

| House | Width | Depth | Wall height | Ridge height | Roof pitch |
|---|---|---|---|---|---|
| Chapel nave | 10 (gable end) | 12 | 9 | 15 | 50° |
| Chapel tower | 5.4 | 4.6 | 18.7 | 25.2 with top plate and spire | spire 6.2 tall |
| Bakery | 13 (gable front) | 9 | 10 | 15.6 | 41° |
| Cottage | 12 (gable front) | 7.6 | 7 | 12 | 40° |

### Openings

Sills are measured from the bottom edge of the wall. Positions are measured from the wall's centre line.

| House | Opening | Size | Sill | Position | LEDs |
|---|---|---|---|---|---|
| Chapel | Side windows, arched, right wall | 1.8 × 4.0 | 3.2 | 2.5 either side | Red (PCA 0) back, green (PCA 1) front |
| Chapel | Tower window, arched | 2.2 × 4.6 | 6.1 | centre | Blue (PCA 2) |
| Chapel | Belfry arches, front and sides | 4.0 and 3.2 wide, 3.0 tall | 15.0 | centre | Bell servo (PCA 13) |
| Chapel | Door | 2.2 × 3.6 | 0 | centre | Painted or dark card, not cut |
| Bakery | Shop window | 7.4 × 3.1 | 1.45 | centre | 2 yellow (PCA 3) |
| Bakery | Upstairs windows | 2.0 × 2.2 | 6.5 | 3.5 either side | 2 yellow (PCA 4) |
| Cottage | Windows | 2.0 × 2.2 | 2.9 | 3.2 either side | 2 yellow (PCA 5) |
| Cottage | Hearth | 1.8 × 1.6 | 1.3 | centre | Red + yellow flicker (PCA 6, 7) |

### Light separation

- Chapel: a nave divider across the middle keeps red and green apart. The tower has its own walls, so blue stays separate. A shelf at 14.6 closes the tower under the belfry and carries the bell servo. The bell servo is an SG90 (about 2.3 × 1.2 × 2.3 cm), so it fits on the shelf with room to spare.
- Bakery: an upstairs floor, top face at 5.6, on two supports in the back corners. Upstairs LED wires run down through a hole at the back of the floor.
- Cottage: a foil-lined hearth box (thin card) behind the hearth window. The window LEDs sit outside it.

### Chimneys

| House | Size | Position | Top height | Face heights above roof |
|---|---|---|---|---|
| Bakery | 1.7 × 1.7 | 3.8 right of the ridge | 16.2 | 2.75 uphill, 4.2 downhill |
| Cottage | 1.8 × 1.8 | 3.6 right of the ridge | 12.7 | 2.55 uphill, 4.05 downhill |

## Material needed

- Bookbinding board: 4 A5 sheets. The tower front and both tower sides share one sheet, and the chapel right side wall, bakery front gable and cottage front gable take one sheet each. You have 20.
- Corrugated: well under one 1200 × 800 sheet for all three houses.
