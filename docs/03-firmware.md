# Firmware requirements

## Memory limits (ATmega168)
- 14 KB usable flash and 1 KB RAM.
- 46 pixels need 138 bytes of RAM, which fits. The 16 × 16 matrix (768 bytes) would not fit, so it stays out.
- Use Adafruit NeoPixel rather than FastLED, which is larger.
- Keep text in flash with `F()` and keep serial debug messages short.
- Melody tables go in PROGMEM.
- In the Arduino IDE choose board Arduino Nano, processor ATmega168.
- If the firmware outgrows the chip, fall back to an ATmega328P Nano if one is owned, or the Mega.

## Structure
- Non-blocking state machine. No `delay()` in the main loop.
- Phases: Dusk, Evening, Sleigh, Carol, Night.
- Runs on one Nano with a PCA9685.

## Triggers
- Room goes dark (A0, with hysteresis): start Dusk.
- Guest button (D2, debounced): play the carol.

## IR remote (next version, not in the first build)
- Receiver on D3. Proposed keys: OK start or stop the show, 1–5 jump to a phase, arrows up and down for tree speed, arrows left and right for string light mode, * sleigh, # carol, 0 all off.
- Decode with TinyIRReceiver (part of the IRremote package): NEC only, small, uses the D2 interrupt and no timer.
- Don't use the full IRremote receiver. On this chip it takes Timer2, which `tone()` also needs.
- Pixel updates switch interrupts off and would corrupt IR frames. When the 9 ms IR start pulse arrives, pause pixel updates for about 120 ms.
- Key codes vary between remotes. A small test sketch prints each key's code once, then the codes go into the firmware.

## Outputs
- PCA9685 at 60 Hz, shared by LEDs and servos. Slight flicker at very low brightness is accepted.
- Pixels: two chains, D6 with 34 pixels (river 0–3, then string 4–33) and D7 with 12. Cap total draw at about 0.6 A (about a quarter brightness).
- String modes: off, steady warm, twinkle, chase. They apply to D6 pixels 4–33 only.
- River: pixels 0–3 steady blue, for example (0, 40, 255) before the brightness cap. Fades in early in Dusk, stays on through Night, off when the show ends. No colour changes in the first version.
- Hearth: channels 6 and 7 flicker out of step.
- Stepper: half-step, motor at most 15 rpm. In AccelStepper's HALF4WIRE mode the pin order is IN1, IN3, IN2, IN4. De-energise the coils when stopped.
- Sound on D12: `tone()` drives the MH-FMD module if it's passive, otherwise the speaker transistor. The module is active-low, so after `noTone()` set D12 HIGH (silent). For the speaker transistor, LOW is silent. Public-domain tunes only.

## Tree motion
The tree turns continuously through the slip ring. No position tracking is needed.

## Speeds (tree rpm, motor is 3 ×)
| Phase | Tree |
|---|---|
| Dusk | 0 |
| Evening, Sleigh | 3 |
| Carol | 5 |
| Night | 1.5 |

## Sleigh sequence
Parked at -82°. Slow sweep to +82° (about 8 s in the demo), hold, dim the moon, return, restore the moon.
- Ease in and out on every move (for example a smoothstep curve), updating the servo every 20 ms. Sudden starts or stops make the hanging sleigh swing.
- Return trip about 3 s, also eased, while the moon is dimmed.


## Timing
Phase lengths on the concept page are shortened for the demo. Real durations are still to be chosen.

## Risk
Pixel updates block interrupts for about 1 ms for 30 pixels, which may make the stepper tick. If audible, a spare Nano can take over the pixels.

## Candidate libraries
Adafruit PWM Servo Driver, AccelStepper, Adafruit NeoPixel. TinyIRReceiver in the next version.
