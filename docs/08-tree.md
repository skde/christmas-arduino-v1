# Christmas tree: build and templates

Status: drafted 2026-11-17. Sizes match the tree in the 3D model in `concept/concept-page.html`.

Printable 1:1 templates: `drawings/templates/tree-templates.pdf` (9 A4 pages). Print at 100 % on plain paper and check the 5 cm bar. Cut the paper pieces out and trace them onto the card. To regenerate after a change, run `python3 tools/tree-templates.py`, then print `drawings/templates/tree-templates.html` to PDF. The script reuses the page code in `tools/house-templates.py`.

## What it is

The tree is five card cones stacked on a card core tube, standing in the centre of the rink disc and turning with it. It's 27 cm tall from the deck, star included. The 12 tree pixels sit inside the cones and shine out through small round windows. The star is card covered in gold foil. It isn't lit, but it catches the light from the pixels.

## Materials

| Material | Pieces |
|---|---|
| Thin card: cereal box painted dark green, or green craft card 200–250 g | 5 cones (tiers 1–3 in two halves each), core tube, 2 stars |
| Corrugated 3 mm | 2 foot rings |
| Gold foil (chocolate or sweet wrapper) | Star |
| Toothpick | Star stem |
| Cotton wool or white paper | Snow on the foot rings and the tier rims (optional) |

Corrugated can't be rolled into cones this tight, so the cones use thin card.

## Sizes (cm)

All cones are 7.2 tall. Heights are measured from the top of the rink disc.

| Tier | Base across | Rim height | Net arc radius | Sector | Pieces | Pixels |
|---|---|---|---|---|---|---|
| 1 | 16.4 | 2.2 | 10.91 | 271° | 2 halves | 1–4 |
| 2 | 14.0 | 6.1 | 10.04 | 251° | 2 halves | 5–7 |
| 3 | 11.4 | 9.9 | 9.18 | 223° | 2 halves | 8–9 |
| 4 | 8.6 | 13.8 | 8.39 | 185° | 1 | 10–11 |
| 5 | 5.8 | 17.5 | 7.76 | 134° | 1, pointed | 12 |

- Core tube: 22 tall, 1.9 across. Two turns of thin card rolled on a 1.8 cm former (a thick marker), glued all over. The tube is the trunk. Paint the bottom 2.2 cm brown.
- Each cone, except the pointed top one, has a 1.9 cm hole at the top that fits snugly on the tube, plus a 6 mm notch for the pixel wires.
- Foot: two corrugated rings, 5 cm across, glued in a stack on the disc centre. The tube stands in them.
- Star: 3.3 cm across, two layers glued back to back on a toothpick. It sits 1.5 cm deep in the tip of tier 5.

## Pixels

- 12 WS2812B pixels cut from the short strip (the same strip as the river), joined by short 3-wire jumpers. The pixels are numbered 1–12 on the templates in chain order: data enters pixel 1. Check that the arrows on each pixel point onward along the chain.
- They are spread 4-3-2-2-1, bottom to top, each 1.5 cm above its cone's rim, behind a 6 mm window. Their angles follow the golden angle so no two line up, and they stay clear of the cone seams.
- Glue each pixel inside its cone, centred on its window and facing out (hot glue at the edges, keeping glue off the LED). A small piece of tracing paper behind the window softens the dot, if wanted.
- The slip-ring wires (5V, GND, data) come up through the disc centre into the core tube and leave through the slot 2.6–3.8 cm up, inside tier 1. The 470 µF capacitor goes across 5V and GND at pixel 1, inside tier 1.
- Leave about 2 cm of slack in every jumper. Measure the real lengths on the built cones before cutting.

## Assembly

1. Roll and glue the core tube. Let it dry straight.
2. Cut and glue the foot rings. Glue them on the disc centre, over the wire hole. Glue the tube into them, upright.
3. Cut the cone pieces. Score the dashed glue line on each tab. Cut the pixel windows with a 6 mm punch, or a sharp blade.
4. Glue each cone together: each tab goes under the other straight edge. Put all seams at the back when you fit them on the tube.
5. Glue the pixels into the cones and solder the chain while the cones are still separate: pixel 1 to 4 in tier 1, then on to tier 2, and so on. Each jumper to the next tier runs up through the notch in the cone below.
6. Thread the cones onto the tube from the top, tier 1 first, and push each one down to its "tier N top" mark. Fix the hole edge to the tube with hot glue. Tier 5 sits over the end of the tube.
7. Feed the slip-ring wires up through the disc and the tube, out through the slot, and solder them to pixel 1 with the capacitor.
8. Test all 12 pixels before adding snow. Then push the star into the tip.

## Balance

The tree turns at 3–5 rpm, so keep it centred and upright: check it from two sides before the glue sets. Card and 12 pixels weigh well under 100 g, so the drive has plenty of margin.
