# micro:bit mini-car receiver

A BBC micro:bit MakeCode project that receives tilt-control radio messages and drives a Keyestudio Mini Car.

This repository is the receiver/car counterpart to the separate `mini-car-remote` transmitter project. The receiver listens for named radio values `x` and `y`, maps them into steering/drive motor commands, and provides simple LED/sound status feedback.

The implementation dates from July 2023. This documentation describes the code currently present on `master`; it does not imply that the historical MakeCode target, Mini Car extension or hardware behaviour has been revalidated with current tooling.

## Startup

The authoritative Blocks/TypeScript implementation:

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
| `x` | Steering / differential-turn input from remote accelerometer X. |
| `y` | Forward/backward drive input from remote accelerometer Y. |

A compatible transmitter should use radio group **20** and send values in the same raw accelerometer range used by MakeCode.

The companion `mini-car-remote` repository does exactly that, nominally every 50 ms per axis.

## Steering control (`x`)

The receiver uses a steering dead zone of approximately `-500..500`.

### X < -500

- M1: Backward
- M2: Forward
- speed magnitude mapped toward 255 as X approaches -1023

This produces a differential/pivot turn.

### X > 500

- M1: Forward
- M2: Backward
- speed magnitude mapped from 0..255 as X moves from 500..1023

### -500 <= X <= 500

Both motors are commanded to speed 0.

## Drive control (`y`)

The receiver uses a smaller drive threshold of approximately `-250..250`.

### Y < -250

Both motors run **Forward**, with speed mapped from 0 at -250 to 255 near -1023.

### Y > 250

Both motors run **Backward**, with speed mapped from 0 at 250 to 255 near 1023.

### -250 <= Y <= 250

The current implementation sends **no motor command** for Y in this neutral range.

That means a prior forward/backward Y command can remain active until another command changes motor output. In practice, incoming X values in their neutral zone may stop both motors because the X handler explicitly writes speed 0, but there is no dedicated receiver-side neutral/failsafe state machine.

## Interaction between X and Y messages

The transmitter sends X and Y as separate radio messages. Each received message immediately updates motor state independently.

That creates an important control characteristic:

- an X packet can overwrite motor commands previously set by Y;
- a Y packet can overwrite motor commands previously set by X;
- there is no atomic combined steering+throttle sample or mixer.

This is acceptable for a simple demo but is not equivalent to coordinated two-axis vehicle control.

## Source authority

The repository contains `main.blocks`, `main.ts`, and `main.py`.

The Blocks and TypeScript representations agree on the main behaviour and configure **radio group 20**.

`main.py` differs in two important ways:

- it configures **radio group 22**;
- in the X neutral branch it sets M2 direction to Backward at speed 0, while Blocks/TypeScript use Forward at speed 0.

Because `pxt.json` declares `blocksprj` as the preferred editor and Blocks/TypeScript agree, this documentation treats **`main.blocks` + `main.ts` as the behavioural authority**.

## Platform and dependency

`pxt.json` records:

- MakeCode target: BBC micro:bit
- target version: `6.0.15`
- preferred editor: `blocksprj`
- dependencies: `core`, `radio`, `microphone`
- Keyestudio Mini Car extension pinned to:
  `github:keyestudio2019/MiniCar#6a11b75a8fd87ccce69f3d02ed5c1666aaa25e1e`

The Mini Car extension supplies the `MiniCar.motor` and RGB LED APIs used here.

## Editing in MakeCode

To edit the project:

1. Open the MakeCode micro:bit editor.
2. Choose **Import** → **Import URL**.
3. Enter the GitHub repository URL for `NickAskewGH/mini-car`.

Prefer editing through MakeCode and review all generated representations after saving, especially the existing Python discrepancies.

## PXT command line

The Makefile contains:

```bash
make build    # pxt build
make deploy   # pxt deploy
make test     # pxt test
```

A compatible MakeCode/PXT toolchain must already be installed. The repository does not pin the Node/PXT environment.

`test.ts` is only a placeholder and provides no meaningful behavioural test coverage.

## Safety considerations

This code directly drives motors from radio input and lacks a robust receiver-side failsafe.

Before using it on a powered vehicle, consider adding or externally enforcing:

- timeout-based motor stop when radio input goes stale;
- an explicit neutral/stop command;
- combined/atomic steering+throttle state;
- validation/clamping of received values;
- startup-safe motor state;
- emergency/manual stop;
- maximum speed limits appropriate to the test environment.

Initial testing should be performed with wheels lifted or otherwise prevented from causing unintended motion.

## Repository structure

- `main.blocks` — authoritative Blocks representation.
- `main.ts` — matching TypeScript representation.
- `main.py` — stale/inconsistent Python representation.
- `pxt.json` — target/dependency/editor metadata.
- `Makefile` — PXT build/deploy/test wrappers.
- `test.ts` — placeholder test file.
- `_config.yml` / `Gemfile` — MakeCode-generated GitHub Pages/Jekyll support.
- `.vscode/` — editor convenience settings.

## Known limitations

- Experimental 2023 project with no current release/versioning policy.
- No substantive automated tests.
- No current hardware/toolchain revalidation evidence in the repository.
- `main.py` disagrees with Blocks/TypeScript on radio group and one zero-speed direction.
- No radio timeout/failsafe.
- Y neutral range does not explicitly stop motors.
- X and Y are processed as independent messages rather than a combined control state.
- No acknowledgement or telemetry back to the remote.
- Motor mapping assumes the current physical motor orientation/wiring.
- Status LEDs/sound are cosmetic and do not indicate radio health.

## Further technical documentation

See [`docs/technical-notes.md`](docs/technical-notes.md) for exact mapping details, receiver-protocol implications, source reconciliation and a manual verification checklist.
