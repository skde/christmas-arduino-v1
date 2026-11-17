# Turntable mechanism

Status: design, not built. Heights depend on the slip ring's real size, so measure it when it arrives (see the end of this file).

## Goals
- Tree and rink turn slowly and steadily, about 3 rpm (one turn every 20 s).
- Tree lights are powered and controlled through the slip ring.
- The whole drive is one unit fixed in the base. The deck lifts off without taking anything apart.
- Quiet enough for a living room.

## Layout

Drawing: [turntable-section.svg](../drawings/turntable-section.svg). Open it in a browser.

The rink disc sits in a round hole in the deck, flush with the deck surface, like a real rink. The hole is about 5 mm wider than the disc. The deck lifts straight off over it.

Everything below the disc is screwed to one drive plate, held about 4.5 cm above the base floor on two wooden blocks.

```
                    tree
     ════════════════════════════════      rink disc, 22 cm, flush with deck
  ───────────┐      ┌▓▓┐      ┌──────────  deck, hole 22.5 cm, lifts off
             │      │▓▓│ ← 8 mm flange coupling, 4 screws into the disc
             │      │  │ ← 8 mm brass tube, wires run inside
   [20T]═════╪═belt═[60T]                  GT2 belt, 3:1
   [ 28BYJ ] │      [KFL08]                upper flange bearing
  ━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━  drive plate, 6 mm plywood
                    [KFL08]                lower flange bearing
                     ║ ← short silicone hose: flexible coupling
                    [rotor]                slip ring, turning part
                    [ body ]               slip ring, fixed part
  ═══════════════════╧═══════════════════  base floor, flange screwed down
                     └─ 6 wires to the Nano and 5V rail
```

Approximate heights from the base floor: drive plate top at 4.5 cm, pulleys at 6.5–7.5 cm, deck at 9 cm. Adjust the blocks under the drive plate once the slip ring's length is known. The deck is about 6 mm thick (two corrugated layers), so its top sits about 9.6 cm above the base floor if it rests on the 9 cm walls. Set the disc top level with that.

## Parts

### Recommended: standard 3D-printer parts
These are common, cheap and fit together without drilling or gluing. Set screws hold everything.

| Part | Job | Approx. |
|---|---|---|
| 2 × KFL08 flange bearing, 8 mm bore | Hold the tube upright, stop wobble and up/down play | €3 |
| GT2 pulley, 20 teeth, 5 mm bore | On the stepper shaft | €1.5 |
| GT2 pulley, 60 teeth, 8 mm bore | On the tube | €2.5 |
| GT2 closed belt, 200 mm, 6 mm wide | Drive | €1.5 |
| 8 mm rigid flange coupling | Fixes the disc to the tube, removable with 4 screws | €2 |
| Brass tube, 8 mm outside, about 6 mm inside, 15 cm | Axle with wires inside | €3 |
| Silicone or aquarium hose, 5 cm | Flexible link from tube to slip ring | €1 |
| 6 mm plywood, about 15 × 10 cm, plus 2 blocks | Drive plate | €2 |
| **Total** | | **about €17** |

### Zero-cost fallback: parts already owned
- Two 608 skate bearings set in layers of glued card instead of KFL08 (608 bearings still needed, about €1 each).
- Large gear or pulley from the gear kit on the tube, drilled out to 8 mm and glued.
- Small pulley from the kit on the stepper, drilled to 5 mm and glued on the shaft flats.
- Rubber band from the kit as the belt.
- Works, but drilling plastic gears straight is hard, glue joints loosen, and belt tension drifts as card flexes. Expect more wobble and fiddling.

## Why this layout
- **No direct drive.** The stepper can't sit on the tree's axis, because the slip ring and the wires need that space. A belt moves the motor to the side.
- **Belt, not gears.** A toothed belt is quiet, tolerates small misalignment and doesn't slip. Plastic gears from the kit would be louder and need precise spacing.
- **Two bearings, about 3 cm apart.** One bearing alone lets a 22 cm disc tilt. Two bearings on either face of the plate hold the tube straight.
- **The bearings carry all the load.** A capsule slip ring is not built for weight or side force. The silicone hose only turns it, and absorbs any misalignment between tube and ring.
- **One drive plate.** Belt tension stays fixed because motor and tube are screwed to the same rigid plate. Cardboard would flex.

## Numbers
- Pulleys: 20T is 12.7 mm and 60T is 38.2 mm pitch diameter, so the ratio is exactly 3:1.
- Centre distance for a 200 mm GT2 belt: about 58.6 mm. Make the motor's two screw holes slotted, a few mm long, to set the tension.
- Tree at 3 rpm means motor at 9 rpm, about 610 half-steps per second. The 28BYJ-48 tops out around 15 rpm, so the tree can reach about 5 rpm.
- Torque: the 28BYJ-48 gives roughly 0.03 N·m at low speed, about 0.1 N·m at the tree after the 3:1 belt. A card tree on two ball bearings needs far less.

## Noise
- Put rubber or foam washers between the motor and the plate, and foam under the plate's blocks. The base box otherwise amplifies motor hum.
- Use half-stepping and switch the coils off when the tree stops.

## Wires
- Tree side: the slip ring's rotor wires run up through the tube, out through a hole in the centre of the flange coupling and the disc, then to the tree strip. A 470 µF capacitor sits at the strip.
- Fixed side: the body's wires go to the 5V rail, GND and D7 (through 330 Ω).
- Use 2 wires for 5V, 2 for GND, 1 for data, 1 spare.

## Measure when the slip ring arrives
- Outside diameter of the rotating collar, to choose the hose size.
- Body length and flange height, to set the drive plate height.
- Flange screw-hole spacing.
- Rated current per wire, expected to be well above the tree strip's 0.2 A.

## Assembly order
1. Mount both KFL08 bearings on the drive plate, centred on one hole.
2. Slide the tube through, fit the 60T pulley between upper bearing and deck height, and lock the bearing set screws.
3. Mount the stepper with its 20T pulley level with the 60T pulley, fit the belt and set the tension.
4. Fix the drive plate on its blocks, with the tube centred under the deck hole.
5. Screw the slip ring flange to the floor under the tube and join it with the silicone hose.
6. Run the wires up the tube, fit the flange coupling and screw on the disc.
7. Test-run the motor for an hour before adding the tree.
