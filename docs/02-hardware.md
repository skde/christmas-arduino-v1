# Hardware

Status: drafted, not built or tested. Check against the real boards before powering on.

## Controller
One Arduino Nano with a PCA9685 board. The user's Nano has an ATmega168: same pins and timers as the ATmega328P, but half the memory (16 KB flash with about 14 KB usable, 1 KB RAM). A spare Nano can take over the pixels only if the stepper ticks during LED updates.

## Nano pins
| Pin | Job | Note |
|---|---|---|
| A4, A5 | I²C to PCA9685 (SDA, SCL) | 11 LED channels, 2 servos, 3 spare |
| D6 | River pixels, then string lights (one chain) | 330 Ω in line |
| D7 | Tree lights data | 330 Ω in line, through the slip ring |
| D8–D11 | Stepper IN1–IN4 | Through ULN2003 board |
| D12 | Sound | MH-FMD module I/O (VCC to 5V, GND to GND), or speaker transistor base through 1 kΩ |
| D2 | Guest button | INPUT_PULLUP, other leg to GND |
| D3 | Reserved for the IR receiver (next version) | Interrupt pin, needed by TinyIRReceiver |
| A0 | Light sensor | 5V to LDR to A0, A0 through 10 kΩ to GND |
| D4, D5, D13, A1–A3 | Spare | |

## PCA9685 channels (address 0x40)
| Channel | Connected to | LED | Extra resistor |
|---|---|---|---|
| 0 | Chapel side window | Red | 100 Ω |
| 1 | Chapel side window | Green | None |
| 2 | Chapel tower window | Blue | None |
| 3 | Bakery shop window | 2 yellow, parallel | 100 Ω |
| 4 | Bakery upstairs | 2 yellow, parallel | 100 Ω |
| 5 | Cottage windows | 2 yellow, parallel | 100 Ω |
| 6 | Hearth | Red | 100 Ω |
| 7 | Hearth | Yellow | 100 Ω |
| 8 | Street lamps | 2 yellow, parallel | 100 Ω |
| 9 | Moon | Yellow | 100 Ω |
| 10 | Stars | 2 blue, parallel | None |
| 11 | Spare | | |
| 12 | Sleigh servo | Plug into header | None |
| 13 | Bell servo | Plug into header | None |
| 14, 15 | Spare | | |

- LED long leg to the channel's PWM pin, short leg to its GND pin. Leave V+ unused.
- Assumes the usual 220 Ω resistor on each board output, giving about 9 mA per channel (10 mA source limit). If the board has none, add 220 Ω to every LED channel.
- Connect VCC and the V+ terminal to the 5V rail, GND to GND, leave OE unconnected.
- Solder 470 µF across the V+ terminal.

## Deck plugs
Every wire group that crosses the deck gets a small plug just under it, so the deck lifts off. Each house shares one GND wire. All PCA9685 GND pins are joined, so a shared return works the same as separate ones. The concept page shows these with "Show wires and plugs".

| Plug | Wires | Contents |
|---|---|---|
| Chapel nave | 3 | PCA 0 +, PCA 1 +, GND |
| Chapel tower | 5 | PCA 2 +, GND, bell servo cable (PCA 13) |
| Bakery | 3 | PCA 3 +, PCA 4 +, GND |
| Cottage windows | 2 | PCA 5 +, GND |
| Cottage hearth | 3 | PCA 6 +, PCA 7 +, GND |
| Lamp left, lamp right | 2 each | PCA 8 +, GND, the two lamps in parallel |
| Moon and stars | 3 | PCA 9 +, PCA 10 +, GND |
| River, string lights | 3 | 5V, GND, D6 data |
| Sleigh servo | 3 | Servo cable (PCA 12) |
| Light sensor | 2 | 5V, A0. The 10 kΩ to GND stays in the base |

That makes 31 wires in 11 plugs. The tree's 3 wires go through the slip ring instead.

## D6 pixel chain
- Order: Nano D6, 330 Ω, deck plug, 4 river pixels in the light box under the ice, then on to the 30 string-light pixels.
- One 3-pin deck plug serves the whole chain. Feed 5V and GND to the river pixels and run them on with the data line to the string.
- Buy the string and the strip as the same WS2812B type, so the colour order (usually GRB) matches.
- The buzzer or speaker board must sit clear of the river light box, which hangs about 4 cm below the deck near the back.

## Turntable
Full mechanism design: [06-turntable.md](06-turntable.md).

- 28BYJ-48 stepper with ULN2003 board, rubber washers between motor and plate.
- GT2 belt, 20T to 60T pulley, 3:1 reduction.
- Axle: 8 mm brass tube in two KFL08 flange bearings on one plywood drive plate.
- Rink disc sits flush in a deck hole, so the deck lifts off freely.
- Slip ring: 6-wire capsule ring with flange (GOCO SRC-22 series, ordered). Use 2 wires for 5V, 2 for GND, 1 for data, 1 spare.
- Mounting: the flange (fixed part) screws to the base floor under the axle. The rotating collar joins the tube with a short silicone hose, and its wires run up the tube to the tree.
- The bearing carries the tree's weight. The slip ring only turns, and never carries load or side force.
- Tree turns continuously.
- 470 µF at the tree strip.
- If data glitches through the slip ring, the fallback is two turns each way with the slip ring bypassed by slack wire.

## Power
- 5 V adapter rated 3 A or more, inline 3 A fuse, shared 5V and GND rails. All grounds joined.
  - Chosen: the user's 5 V 5 A notebook-style adapter (5.5/2.1 mm plug), found 2026-11-16. The label output (5 V, 5 A) was read by the user on 2026-11-16. Before first use, check centre-positive polarity and measure about 5.0–5.3 V unloaded. Enough for the 16 × 16 matrix too, if it's ever added. It needs a matching 5.5/2.1 mm female socket in the base. A higher rating is safe because the load draws only what it needs, and the 3 A fuse still protects the wiring.
  - Also fine: a USB-C charger of 15 W or more (gives 5 V 3 A), with a USB-C breakout board that has 5.1 kΩ CC resistors and power wires 0.5 mm² or thicker. A Raspberry Pi 4 supply (5.1 V 3 A) works this way too.
  - Don't use 5 V 2 A or 2.5 A adapters, an old USB-A phone charger, or a 12 V adapter with the XL6009 (it steps up only).
- Main power switch: the owned rocker switch (IMG_1061), set in the left side wall of the base, level with the power board (z ≈ 12), so it is hidden when the scene is viewed from the front. Wiring: DC socket + → switch → 3 A fuse → 5V rail. GND is not switched. Check the rating printed on it is 3 A or more (typical rockers are 6–10 A).
- 1000 µF across the rail.
- Nano joins the rail through removable link J1. Remove J1 whenever USB is plugged in.
- Keep the adapter outside the box. The switch turns the scene off, but the adapter stays live, so still unplug it when nobody is around.

| Load | Typical | Worst case |
|---|---|---|
| Nano | 0.04 A | 0.04 A |
| 46 pixels, capped in firmware | 0.60 A | 0.60 A |
| Plain LEDs, 11 channels at 9 mA | 0.10 A | 0.10 A |
| Stepper | 0.24 A | 0.24 A |
| 2 servos | 0.40 A | 1.30 A |
| **Total** | **1.38 A** | **2.28 A** |

Uncapped, 46 pixels could draw 2.8 A at full white, so the firmware cap is mandatory.
