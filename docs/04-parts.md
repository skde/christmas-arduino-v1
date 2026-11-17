# Parts

Inventory from 29 photos reviewed 2026-11-06 (photos since removed; `inventory.txt` is the record). Counts are what the photos show, so there may be more.
Prices are rough estimates, not checked against a shop.

## Owned and useful
| Part | Photo | Use |
|---|---|---|
| Arduino Nano, at least 2, headers not soldered | IMG_1073, 1075 | Main controller or pixel controller |
| 28BYJ-48 5 V stepper with ULN2003 board | IMG_1060 | Turntable |
| SG90-type micro servos, several | IMG_1071 | Sleigh and bell |
| WS2812B-type flexible matrix, 16 × 16 (256 pixels), with 3-wire in/out and 2-wire power | IMG_1084 | Optional animated sky, left out of the first version |
| Yellow diffused 5 mm LEDs, about 100 | IMG_1063 | House windows, lamps, moon |
| Red and green 5 mm LEDs, about 100 each | IMG_1074 | Chapel glass, hearth |
| Water-clear 5 mm LEDs, about 100, colour to test | IMG_1074 | Probably the blue LEDs the user mentioned |
| IR remote kit: receiver module and 17-key remote | IMG_1109 | Show control in the next version |
| Tactile buttons with coloured caps | IMG_1062 | Guest button |
| Buzzers, several, active (tested) | IMG_1064 | Unused, beeps only, no melodies |
| MH-FMD buzzer module, active-low, type to test | IMG_1114 | Carol if passive |
| 8 Ω 1 W speaker | IMG_1107 | Carol, louder and works with any tone, needs one transistor |
| Metal film resistor assortment | IMG_1108 | All resistors in the circuit, values to confirm |
| BC547C NPN transistors, about 15 | IMG_1107 | Speaker driver if the buzzer is active |
| Rocker switch | IMG_1061 | Main power switch, left side wall, between DC socket and fuse |
| Screw terminal strip, 6-way | IMG_1077 | 5V and GND rails |
| Perfboard, double-sided | IMG_1059 | Resistors and power board |
| Plastic gears, pulleys, rack, rubber belts | IMG_1066 | Turntable drive. Bores look small for the 5 mm stepper shaft |
| PIR motion sensor (HC-SR501 type) | IMG_1077 | Wake the show when someone approaches |
| 6-pad touch board | IMG_1080 | Optional hidden touch controls |
| Corrugated cardboard, single-wall 3 mm, 1200 × 800 mm sheets, several (bought 2026-11-16) | no photo | Base box, deck, hills, scenery, and the plain house walls, roofs and inner pieces. One sheet gives two 70 × 45 pieces (one turned 90°). Floor plus the two deck layers take 2 sheets, so 3–4 sheets is enough |
| Bookbinding board, A5, 1.5 mm, 20 sheets | no photo | House walls that have windows, for clean cut-outs. 4 of the 20 sheets (see 07-houses.md) |
| 20 × 4 LCD with I²C backpack | IMG_1082, 1083 | Optional greeting or countdown |
| Multi-turn trimmers, about 10 | IMG_1078 | Optional threshold tuning |

## Owned, needs identifying
- White LED strip on a reel, not addressable, voltage not visible (IMG_1086). Could light house interiors. Read the voltage printed on the strip. If 12 V, it needs a boost module and a driver.
- 4-pin sensor board with LM393 and trimmer (IMG_1070). Photo is blurred and the sensor is on the other side.
- Small labelled bag at the top of IMG_1074. Contents unclear.

## Owned, not needed
- XL6009 boost modules (IMG_1071, 1076, 1080): raise voltage only, so they can't supply 5 V from a higher voltage. Useful only for a 12 V strip.
- Arduino Mega 2560 with L293D motor shield (IMG_1069, 1085): free to use, but the Nano with PCA9685 was chosen.
- Micro SD card module (IMG_1107): playing sound files would not fit in the ATmega168.
- Small DC motor (IMG_1068), relay module (IMG_1079), HC-SR04 ultrasonic sensor (IMG_1067), slide switch (IMG_1081).
- nRF24L01 radio, TP4056 charger, battery protection boards (IMG_1080).
- 14500 and 18650 lithium cells and holders, AA holder (IMG_1063, 1072, 1087): avoid lithium cells inside a cardboard model.

## Not seen in the photos
LDR, 1000 µF and 470 µF capacitors, fuse holder, hook-up wire.

The DC barrel plug in IMG_1107 is the male type. A wall adapter also ends in a male plug, so the base needs a female socket.

## To buy
| Part | For | Approx. |
|---|---|---|
| Female DC socket 5.5/2.1 mm with screw terminals | Power, takes the 5 V 5 A adapter | €2 |
| WS2812B string and short strip | String lights, tree and 4 river pixels | €8 |
| Capacitors, fuse holder, small plugs | Power and deck connections | €3 |
| Turntable mechanism parts, see 06-turntable.md | Bearings, belt, pulleys, axle | €17 |
| PCA9685 16-channel PWM board | LED dimming and servos | €4 |
| Capsule slip ring with flange, 6 wires | Tree wiring, already ordered | ordered |
| **Total** | | **€34** |

## Basic components
Resistors, capacitors, diodes, transistors and the LDR are cheap and quick to buy. Add any missing value to the main order rather than tracking it.
