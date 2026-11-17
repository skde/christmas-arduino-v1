# Open questions

The user will answer these later. The project should stay simple and need not use every part in the photos.

- [ ] 16 × 16 matrix: use it at all? Recommended: leave it out of the first version. It can be added later as an animated sky. Don't cut it up.
- [ ] Nanos: do all of them have the ATmega168, or do any have the ATmega328P? The chip name is printed on the square chip. A 328P gives twice the memory.
- [ ] LED strip on the reel: what voltage is printed on it?
- [ ] Buzzer module MH-FMD (IMG_1114): active or passive? Wire VCC to 5V and GND to GND, then touch I/O to GND. A steady beep means active. A single click means passive. If it's passive, it plays melodies and becomes the carol buzzer. If it's active, the speaker fallback below is used.
- [ ] Water-clear LEDs: what colour are they? Test with 5 V through 330 Ω.
- [ ] 4-pin sensor board in IMG_1070: which sensor is it? Needs a sharper photo of the other side.
- [ ] Size: confirm 70 × 45 cm suits the space.
- [ ] PCA9685 board: when it arrives, confirm it has 220 Ω output resistors.
- [ ] Turntable: use the recommended 3D-printer parts (about €17), or the zero-cost version from the gear kit? See 06-turntable.md.
- [ ] Slip ring, when it arrives: measure collar diameter, body length, flange hole spacing and rated current.
- [ ] Real show timing: phase lengths and how often the show repeats.

## Decided
- Corrugated sheets are single-wall, 3 mm (user, 2026-11-17). The deck is two layers glued with the flutes crossed, about 6 mm thick, so it stays flat around the rink hole.
- Servos: two of the user's own SG90s, one for the sleigh and one for the bell (2026-11-17). The robot car keeps its servo.
- Basic components (resistors, capacitors, diodes, transistors, LDR) are cheap and quick to buy, so they are not tracked as open questions. Buy any missing value with the main order.
- User can solder.
- User is willing to buy parts, including addressable LEDs.
- Sound stays a simple buzzer for now.
- Power: the user's 5 V 5 A notebook-style adapter with a 5.5/2.1 mm plug (found 2026-11-16), with the 3 A inline fuse kept.
- Power switch: the owned rocker switch in the left side wall (hidden from the front), switching 5V between the DC socket and the fuse (2026-11-17).
- Loose buzzers (IMG_1064) tested: all active, so they can't play melodies. Unless the MH-FMD module turns out to be passive, melodies come from the 8 Ω speaker plus one BC547C: D12 through 1 kΩ to the base, emitter to GND, speaker and 68 Ω in series from 5V to the collector (about 65 mA peak, within the BC547C 100 mA limit).
- Keep it simple: unused parts stay unused.
- Slip ring ordered (6-wire capsule with flange, GOCO SRC-22 series). The tree turns continuously.
- IR remote: next version, or when the scene has enough modes to need it. The guest button stays on D2, and D3 is kept free for the receiver.
- Controller: one Nano plus PCA9685. No Mega, ESP32 or Wi-Fi.
- Yellow diffused LEDs replace the planned warm white LEDs. These need 100 Ω extra on PCA9685 outputs.
- Transistors are BC547C NPN, suitable for driving the speaker.
- Red, green and blue LEDs: chapel stained glass, hearth, stars.
