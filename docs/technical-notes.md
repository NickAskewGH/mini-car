# Technical notes

## Source reconciliation

Current representations differ as follows:

| Representation | Radio group | X neutral M2 direction | Slide sound |
| --- | ---: | --- | --- |
| `main.blocks` | 20 | Forward @ 0 | Yes |
| `main.ts` | 20 | Forward @ 0 | Yes |
| `main.py` | 22 | Backward @ 0 | No |

`pxt.json` specifies `blocksprj` as the preferred editor. Blocks and TypeScript therefore form the current documentation authority.

The Python file should be treated as stale until it is regenerated/reconciled in MakeCode.

## Radio callback

The receiver registers a named-value handler.

### X branch

For `name == "x"`:

- below -500, M1 and M2 run in opposite directions for a pivot turn;
- above 500, the motor directions reverse relative to the negative branch;
- between -500 and 500, both motor speeds are set to zero.

### Y branch

For `name == "y"`:

- below -250, both motors run Forward;
- above 250, both motors run Backward;
- there is no `else` branch.

The missing Y neutral branch is an important behavioural fact. If the last processed packet was a Y drive command and no subsequent X-neutral packet arrives, that motor command is not explicitly cleared by a neutral Y value.

## Mapping details

The firmware uses MakeCode `Math.map` rather than explicit clamping logic.

The intended ranges are:

- steering threshold magnitude: 500;
- drive threshold magnitude: 250;
- full accelerometer endpoint: approximately 1023;
- motor PWM target: 0..255.

One oddity is visible in the negative-X M1 mapping:

```text
Math.map(value, 500, -1023, 0, 255)
```

while the corresponding M2 mapping starts from -500. This asymmetry is present in Blocks/TypeScript and is documented as-is. It may be intentional tuning or a historical mistake; the repository contains no test/evidence explaining it.

## Companion transmitter

The separate `mini-car-remote` project documents group 20 and sends X/Y accelerometer values nominally every 50 ms.

Because X and Y are sent separately and this receiver acts on each message immediately, steering and throttle are not mixed into one coherent command.

A more robust receiver would retain the most recent X and Y values, apply a freshness timeout, and compute both motor outputs from the combined state.

## Status animation

Every 1000 ms the receiver toggles `led_flip`.

One state sets:

- left car LED red;
- right car LED blue;
- micro:bit Small Diamond.

The other swaps the car LED colours and displays Diamond.

The startup also plays the built-in slide sound in the background in Blocks/TypeScript. `main.py` omits this sound, another sign that the Python representation is stale.

## Radio group discrepancy

Blocks/TypeScript use group 20. Python uses group 22.

The paired transmitter's authoritative Blocks/TypeScript documentation also uses group 20, which reinforces group 20 as the intended current pair configuration.

## Verification status

`test.ts` is only a placeholder.

A useful manual verification sequence is:

1. build/flash both remote and receiver with compatible MakeCode/PXT tooling;
2. keep the car wheels lifted or mechanically constrained;
3. confirm receiver startup icon, slide sound and LED alternation;
4. verify both devices are operating on radio group 20;
5. send neutral X and confirm both motors stop;
6. exercise negative/positive X and verify pivot direction/speed;
7. exercise negative/positive Y and verify forward/backward direction/speed;
8. send neutral Y after a drive command and observe the current lack of explicit stop;
9. interrupt transmitter power/radio and observe that the receiver has no timeout stop;
10. decide on and implement a failsafe before unconstrained driving.

Do not treat successful compilation as proof of safe vehicle behaviour.

## Generated infrastructure

`_config.yml`, `Gemfile`, `.gitignore`, `.vscode/`, and `tsconfig.json` are standard MakeCode/project scaffolding and do not define the vehicle-control behaviour.
