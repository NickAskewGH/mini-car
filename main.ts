const CONTROL_LIMIT = 1023
const MOTOR_LIMIT = 255
const MAX_DURATION_MS = 60000
const PENDING_TIMEOUT_MS = 1000

let leftDemand = 0
let rightDemand = 0
let durationMs = 500
let leftPending = false
let rightPending = false
let durationPending = false
let pendingStarted = 0
let controlStarted = 0
let controlActive = false

function clamp(value: number, minimum: number, maximum: number): number {
    return Math.max(minimum, Math.min(maximum, value))
}

function setMotor(motor: Motorlist, value: number) {
    const speed = Math.round(Math.map(Math.abs(value), 0, CONTROL_LIMIT, 0, MOTOR_LIMIT))
    MiniCar.motor(
        motor,
        value < 0 ? Direction1.Backward : Direction1.Forward,
        clamp(speed, 0, MOTOR_LIMIT)
    )
}

function stopMotors() {
    MiniCar.motor(Motorlist.M1, Direction1.Forward, 0)
    MiniCar.motor(Motorlist.M2, Direction1.Forward, 0)
}

function applyControlDirective() {
    setMotor(Motorlist.M1, leftDemand)
    setMotor(Motorlist.M2, rightDemand)
    leftPending = false
    rightPending = false
    durationPending = false
    controlStarted = input.runningTime()
    controlActive = true
}

radio.onReceivedValue(function (name, value) {
    if (!leftPending && !rightPending && !durationPending) {
        pendingStarted = input.runningTime()
    }

    if (name == "x") {
        leftDemand = clamp(value, -CONTROL_LIMIT, CONTROL_LIMIT)
        leftPending = true
    } else if (name == "y") {
        rightDemand = clamp(value, -CONTROL_LIMIT, CONTROL_LIMIT)
        rightPending = true
    } else if (name == "t") {
        durationMs = clamp(value, 1, MAX_DURATION_MS)
        durationPending = true
    } else {
        return
    }

    if (leftPending && rightPending && durationPending) {
        applyControlDirective()
    }
})
radio.setGroup(20)
radio.setTransmitPower(7)
stopMotors()
basic.showIcon(IconNames.Diamond)
let led_flip = true
music.play(music.builtinPlayableSoundEffect(soundExpression.slide), music.PlaybackMode.InBackground)
loops.everyInterval(1, function () {
    const now = input.runningTime()
    if (controlActive && now - controlStarted >= durationMs) {
        leftDemand = 0
        rightDemand = 0
        controlActive = false
        stopMotors()
    }
    if ((leftPending || rightPending || durationPending) && now - pendingStarted >= PENDING_TIMEOUT_MS) {
        leftPending = false
        rightPending = false
        durationPending = false
    }
})
loops.everyInterval(1000, function () {
    led_flip = !(led_flip)
    if (led_flip) {
        MiniCar.led_rgb(LED_rgb_L_R.LED_L, LED_color.red1)
        MiniCar.led_rgb(LED_rgb_L_R.LED_R, LED_color.blue1)
        basic.showIcon(IconNames.SmallDiamond)
    } else {
        MiniCar.led_rgb(LED_rgb_L_R.LED_L, LED_color.blue1)
        MiniCar.led_rgb(LED_rgb_L_R.LED_R, LED_color.red1)
        basic.showIcon(IconNames.Diamond)
    }
})
