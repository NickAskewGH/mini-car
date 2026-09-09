# micro:bit mini-car receiver

A BBC micro:bit MakeCode project that receives two-axis radio control messages and drives a Keyestudio Mini Car.

This repository is the receiver/car counterpart to the separate `mini-car-remote` transmitter project. The receiver listens for `x`, `y`, and `t` radio values, treats them as one timed direct-wheel command, and provides local duration enforcement plus simple LED/sound status feedback.

The implementation dates from July 2023. This documentation describes the code currently present on `master`; it does not imply that the historical MakeCode target, Mini Car extension or hardware behaviour has been revalidated with current tooling.

## Startup

The authoritative TypeScript implementation:

1. selects MakeCode radio group **20**;
2. sets radio transmit power to **7**;
3. displays the **Diamond** icon;
4. initializes `led_flip = true`;
5. plays the built-in **slide** sound effect in the background;
6. starts a 1-second status animation that alternates the left/right Mini Car LEDs between red/blue and swaps the micro:bit display between Diamond and Small Diamond.

The receiver itself does not transmit control acknowledgements; the transmit-power setting is therefore not used by the control logic shown here.

## Radio protocol

The project receives MakeCode named values:

| Name | Meaning |
| --- | --- |
| `x` | Signed M1/left-wheel demand. |
| `y` | Signed M2/right-wheel demand. |
| `t` | Directive duration in milliseconds. |

A compatible transmitter should use radio group **20** and send values in the range `-1023..1023`. Values can come from an accelerometer or a precise API.

The historical `mini-car-remote` sends accelerometer axes under the same names,
but those values are not direct wheel demands. The direct-wheel receiver is
intended for the HTTP bridge API; the handheld remote would require its own
mixing update to remain intuitive.

## Direct wheel control

Positive values drive a motor Forward, negative values drive it Backward, and
zero stops it. Each signed demand is clamped to `-1023..1023` and mapped directly
to PWM magnitude `0..255`, preserving the finest control the protocol provides.

The receiver applies motor outputs only after all three parts of a fresh directive arrive:

```text
M1 = x
M2 = y
duration = t
```

This prevents the intermediate twitch that occurs when `x` is applied before
the matching `y` and `t` packets. Curves and pivots are requested explicitly by
choosing different signed wheel demands at the API.

## Local duration control

`t` is clamped to `1..60000` ms. The timer starts on the micro:bit only after the
complete directive has arrived and both motor commands have been written. A 1 ms
local interval checks expiry and stops both motors. This excludes host, serial,
and radio delivery latency from the requested movement duration.

Incomplete directives are discarded after one second, and motors are stopped at
startup. A new complete directive replaces the active one and restarts timing.

## Source authority

The repository contains `main.blocks`, `main.ts`, and `main.py`. The finer-grained stateful mixer is authored in `main.ts`, and `pxt.json` now selects `tsprj` as the preferred editor and excludes the stale Blocks/Python artifacts from compilation.

## Platform and dependency

`pxt.json` records:

- MakeCode target: BBC micro:bit
- target version: `6.0.15`
- preferred editor: `tsprj`
- dependencies: `core`, `radio`, `microphone`
- Keyestudio Mini Car extension pinned to:
  `github:keyestudio2019/MiniCar#6a11b75a8fd87ccce69f3d02ed5c1666aaa25e1e`

The Mini Car extension supplies the `MiniCar.motor` and RGB LED APIs used here.

## Editing in MakeCode

To edit the project:

1. Open the MakeCode micro:bit editor.
2. Choose **Import** → **Import URL**.
3. Enter the GitHub repository URL for `NickAskewGH/mini-car`.

Use the JavaScript/TypeScript editor when importing the project. Switching to Blocks may not represent the stateful mixer faithfully.

## PXT command line

The Makefile contains:

```bash
make build    # pxt build
make deploy   # pxt deploy
make test     # pxt test
```

A compatible MakeCode/PXT toolchain must already be installed. The repository does not pin the Node/PXT environment.

`test.ts` is only a placeholder and provides no meaningful behavioural test coverage.

### Flashing micro:bit V2

`pxt build` produces a universal image and board-specific images. For a confirmed
micro:bit V2, prefer the smaller CODAL image:

```text
built/mbcodal-binary.hex
```

The universal `built/binary.hex` also contains V2 code, but its larger transfer
can take longer over the MICROBIT mass-storage interface.

DAPLink error 504 means the USB file transfer timed out; it is not a runtime
panic from this program. If it occurs, wait for the MICROBIT drive to remount,
disconnect and reconnect the board, remove any stale `FAIL.TXT` by completing a
successful flash, and copy `mbcodal-binary.hex` again. Do not start another copy
while the activity LED is flashing. Repeated 5xx errors may require updating the
board's DAPLink interface firmware.

## Safety considerations

This code directly drives motors from radio input. It clamps inputs, stops at startup, mixes both axes in one control loop, and expires stale axes after 500 ms. These protections do not replace an independent emergency/manual stop or a maximum speed suitable for the test environment.

Initial testing should be performed with wheels lifted or otherwise prevented from causing unintended motion.

## Repository structure

- `main.ts` — authoritative, compiled TypeScript representation.
- `main.blocks` — historical pre-mixer Blocks representation.
- `main.py` — historical pre-mixer Python representation.
- `pxt.json` — target/dependency/editor metadata.
- `Makefile` — PXT build/deploy/test wrappers.
- `test.ts` — placeholder test file.
- `_config.yml` / `Gemfile` — MakeCode-generated GitHub Pages/Jekyll support.
- `.vscode/` — editor convenience settings.

## Known limitations

- Experimental 2023 project with no current release/versioning policy.
- No substantive automated tests.
- Builds successfully with `pxt-microbit` 9.1.1; proportional motor behavior
  and timeout handling still require raised-wheel hardware validation.
- Blocks/Python artifacts are stale and intentionally excluded from compilation.
- The x/y/t packets are separate and have no sequence number; the receiver groups
  the next fresh value of each name in arrival order.
- No acknowledgement or telemetry back to the remote.
- Motor mapping assumes the current physical motor orientation/wiring.
- Status LEDs/sound are cosmetic and do not indicate radio health.

## Further technical documentation

See [`docs/technical-notes.md`](docs/technical-notes.md) for exact mapping details, receiver-protocol implications, source reconciliation and a manual verification checklist.
