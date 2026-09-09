# Technical notes

## Source authority

`main.ts` is the source of truth. `pxt.json` uses `tsprj` and compiles only
`main.ts` plus the README. The Blocks and Python files preserve the historical
threshold controller but are not compiled.

## Radio callback

The named-value callback clamps `x` and `y` as direct signed M1 and M2 demands,
and clamps `t` to `1..60000` ms. It updates both motors only after one fresh value
for each name has arrived, preventing intermediate radio packet state from
reaching the wheels.

## Mapping details

Each wheel demand is clamped to ±1023 and mapped proportionally to PWM magnitude
`0..255`. Positive demand is Forward and negative demand is Backward.

The mapping is direct:

```text
M1 = x
M2 = y
```

Representative approximate PWM results are:

| x | y | M1 | M2 |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 |
| 600 | 600 | +150 | +150 |
| -600 | -600 | -150 | -150 |
| 600 | 300 | +150 | +75 |
| 1023 | -1023 | +255 | -255 |

Positive values mean Forward and negative values mean Backward.

## Companion transmitter

The separate `mini-car-remote` project uses group 20 and sends accelerometer X/Y
values nominally every 50 ms. Those semantics differ from direct wheel demands;
this receiver profile targets the HTTP bridge API.

X, Y, and T are separate `sendValue` packets. The receiver waits for a complete
fresh triplet, writes both motors, and then records `input.runningTime()` as the
directive start. A 1 ms local interval stops both motors when elapsed time reaches
T. Partial triplets are discarded after one second.

## Status animation

Every 1000 ms the receiver toggles `led_flip`.

One state sets:

- left car LED red;
- right car LED blue;
- micro:bit Small Diamond.

The other swaps the car LED colours and displays Diamond.

The startup also plays the built-in slide sound in the background in Blocks/TypeScript. `main.py` omits this sound, another sign that the Python representation is stale.

## Radio group

The authoritative TypeScript and paired transmitter use group 20. Historical
generated representations are excluded from compilation.

## Verification status

`test.ts` is only a placeholder.

A useful manual verification sequence is:

1. build/flash both remote and receiver with compatible MakeCode/PXT tooling;
2. keep the car wheels lifted or mechanically constrained;
3. confirm receiver startup icon, slide sound and LED alternation;
4. verify both devices are operating on radio group 20;
5. send `x=0, y=0` and confirm both motors stop;
6. increase positive and negative X with Y at zero and verify proportional M1 control;
7. increase positive and negative Y with X at zero and verify proportional M2 control;
8. send equal signed values and verify straight forward/backward movement;
9. send unequal values and verify proportional curves and pivots;
10. compare nearby durations such as 1025 and 1050 ms and verify locally timed stopping;
11. send an incomplete triplet and verify it does not alter motor output.

Do not treat successful compilation as proof of safe vehicle behaviour.

## Generated infrastructure

`_config.yml`, `Gemfile`, `.gitignore`, `.vscode/`, and `tsconfig.json` are standard MakeCode/project scaffolding and do not define the vehicle-control behaviour.
