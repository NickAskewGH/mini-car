radio.onReceivedValue(function (name, value) {
    if (name == "x") {
        if (value < -500) {
            MiniCar.motor(Motorlist.M1, Direction1.Backward, Math.map(value, 500, -1023, 0, 255))
            MiniCar.motor(Motorlist.M2, Direction1.Forward, Math.map(value, -500, -1023, 0, 255))
        } else if (value > 500) {
            MiniCar.motor(Motorlist.M1, Direction1.Forward, Math.map(value, 500, 1023, 0, 255))
            MiniCar.motor(Motorlist.M2, Direction1.Backward, Math.map(value, 500, 1023, 0, 255))
        } else {
            MiniCar.motor(Motorlist.M1, Direction1.Forward, 0)
            MiniCar.motor(Motorlist.M2, Direction1.Forward, 0)
        }
    } else if (name == "y") {
        if (value < -250) {
            MiniCar.motor(Motorlist.M1, Direction1.Forward, Math.map(value, -250, -1023, 0, 255))
            MiniCar.motor(Motorlist.M2, Direction1.Forward, Math.map(value, -250, -1023, 0, 255))
        } else if (value > 250) {
            MiniCar.motor(Motorlist.M1, Direction1.Backward, Math.map(value, 250, 1023, 0, 255))
            MiniCar.motor(Motorlist.M2, Direction1.Backward, Math.map(value, 250, 1023, 0, 255))
        }
    }
})
radio.setGroup(20)
radio.setTransmitPower(7)
basic.showIcon(IconNames.Diamond)
let led_flip = true
music.play(music.builtinPlayableSoundEffect(soundExpression.slide), music.PlaybackMode.InBackground)
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
