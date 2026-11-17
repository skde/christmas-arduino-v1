# Concept

## Model
- Base: shallow box, 70 × 45 × 9 cm, with a removable cardboard deck. The deck is two layers of the 3 mm single-wall corrugated, glued with the flutes crossed (about 6 mm), so it stays flat around the rink hole.
- All electronics stay in the base. Wires crossing the deck use plugs so it can lift off.
- Materials: corrugated card (base, deck, scenery, plain house walls and roofs), bookbinding board (house walls with windows), paper, tissue, tracing paper, foil.

## Elements
| Element | Build | Behaviour | Driven by |
|---|---|---|---|
| Chapel, 25 cm tall | Card, red/green/blue tissue windows | Stained glass fades up, bell swings during carol | 3 LED channels, 1 servo |
| Bakery | Card, paper awning, tracing paper windows | Shop and upstairs light separately | 2 LED channels |
| Cottage | Card, tracing paper, hearth window | Windows light, hearth flickers | 3 LED channels |
| Rink and tree, 27 cm tall | 22 cm foil disc, 5 stacked thin-card cones on a card core tube (08-tree.md), paper skaters | Turns continuously, tree lights twinkle | Stepper, 12 pixels |
| String lights | Addressable string on thin wire, on 2 posts and 2 walls | Steady, twinkle or chase | 30 pixels |
| Street lamps | 2 card posts | Steady light | 1 LED channel |
| Frozen river and bridge | 4 cm slot in the deck along the foot of the front hills, frosted clear plastic over tracing paper, card trough below. Card footbridge | Ice glows steady blue from below | 4 pixels, first on the D6 chain |
| Sledding children | 3 card figures and a white sled run on the front ridge face | Static | Nothing |
| Snowman, about 6.5 cm | Polystyrene or cotton-wool balls, card hat, felt scarf, twig arms | Static | Nothing |
| Sleigh | Card cut-out on a 28 cm skewer arm, hinged to stay level | Crosses the sky from left hill to right hill | 1 servo |
| Moon and stars | Backdrop with tracing-paper moon and pinholes | Backlit, moon dips during the sleigh's return | 2 LED channels |
| Inputs | Button on front wall, light sensor on deck | Dark room starts the show, button plays the carol | 2 pins |

## Show
1. Dusk: room goes dark, river ice and windows come on in turn.
2. Evening: lights twinkle, tree turns.
3. Sleigh: servo carries it across the sky.
4. Carol: bell swings, buzzer plays, lights chase.
5. Night: windows go out, tree and river stay lit.

## Next version
- IR remote control, when the scene has enough modes to need it. The kit is owned and D3 stays free for it.

## Frozen river and bridge
Added 2026-11-17.

- Placement: along the foot of the front hills, between the chapel and the bakery, from about x = -15 to +13 cm from the deck centre. Both ends bend back and slip behind the front ridge, so the river seems to flow out of the scene into the mountains.
- The front ridge moves back 1.5 cm, to about 7 cm from the back edge, to make room. The sleigh servo behind it still clears.
- River slot: about 4 cm wide in the middle, narrowing to about 2.5 cm at the ends for depth. In the middle it runs about 8–12 cm from the back edge. That leaves about 2.5 cm of deck between the slot and the rink hole, so don't move it further forward.
- Ice, from bottom to top: tracing paper as a diffuser, then clear plastic (a blister pack, PET sheet or CD case), sanded on top for frost. Optionally score a few cracks from below with a knife. White paper or baking-soda snow along both banks hides the cut edge.
- Light box: a card trough about 4 cm deep, glued under the slot and lined with foil or white paper. Its walls also stiffen the deck next to the rink hole. It lifts off with the deck, using one 3-pin plug (5V, GND, data) like the other deck wires.
- Light: 4 WS2812B pixels on the trough floor, spaced about 7 cm apart, facing up. Cut them from the short strip and join them with short 3-wire jumpers.
- Colour: a steady blue in the first version, with no colour changes. It fades in at Dusk and stays on through Night. Shimmer or colour changes can come later in firmware alone, with no rewiring.
- Bridge: a small arched footbridge, about 6 cm long and 2.6 cm wide, cut from bookbinding board, with card posts and a rail. It runs from the rink path across the river, and its far end rests against the front ridge. Glue both ends to the deck.

## Sledding children and snowman
Added 2026-11-17. Static decorations, no electronics.

- Sled run: a white paper strip about 1.5 cm wide, running diagonally down the front ridge face to the river bank, to the right of the bridge, about 2–11 cm right of the deck centre. Draw two thin grey sled tracks on it.
- Children, about 2–3 cm tall, cut from card and painted, each with a small card tab behind so they stand off the hill and cast a shadow:
  - one halfway down on a sled, leaning back;
  - one at the top standing beside a sled, about to push off;
  - one beside the lower part of the run, pulling an empty sled back up on a thread.
- They're lit by the river's blue glow and need no LEDs.
- Moving children are a next-version idea. The gap behind the front ridge is taken by the sleigh arm, so it would need a second servo (PCA channel 14) with a magnet under the deck, or its own small hill in front of the ridge.
- Snowman: about 6.5 cm tall, in the open snow in front of the bakery, about 22 cm right of centre and 9 cm in front of the middle. Make it from three polystyrene or cotton-wool balls on a toothpick, with pinhead eyes and buttons, an orange card nose, a black card top hat, a red felt scarf and twig arms. Glue it to the deck through a toothpick end.

## Sleigh mechanism
- The sleigh hangs from a free pivot pin at the tip of the arm, like a Ferris wheel gondola. Gravity keeps it level as the arm swings.
- The pivot sits above the sleigh's centre of gravity, including the reindeer. Find the spot by hanging the cut-out from a pin and moving the hole until it hangs level. A small weight low in the sleigh, such as a washer, makes it steadier.
- A slightly snug pivot, with a felt or paper washer, damps swinging.
- The arm must start and stop gently, or the sleigh swings like a pendulum. See the easing in 03-firmware.md.
- The sleigh hangs below the arm tip. Check it clears the hills when parked at each end.
- Paint the arm dark blue so it disappears against the sky.
- Rigid alternative, if swinging is a problem: a parallelogram linkage, with a second arm parallel to the first, holds the sleigh exactly level with no swing.

## Known limit
The sleigh arm returns along the same path, so the sleigh would fly backwards. The show dims the moon while the arm returns. The return can't be too fast, or the hanging sleigh swings.
