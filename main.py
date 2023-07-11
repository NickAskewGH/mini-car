def on_received_value(name, value):
    if name == "x":
        if value < -500:
            MiniCar.motor(Motorlist.M1,
                Direction1.BACKWARD,
                Math.map(value, 500, -1023, 0, 255))
            MiniCar.motor(Motorlist.M2,
                Direction1.FORWARD,
                Math.map(value, -500, -1023, 0, 255))
        elif value > 500:
            MiniCar.motor(Motorlist.M1,
                Direction1.FORWARD,
                Math.map(value, 500, 1023, 0, 255))
            MiniCar.motor(Motorlist.M2,
                Direction1.BACKWARD,
                Math.map(value, 500, 1023, 0, 255))
        else:
            MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 0)
            MiniCar.motor(Motorlist.M2, Direction1.BACKWARD, 0)
    elif name == "y":
        if value < -250:
            MiniCar.motor(Motorlist.M1,
                Direction1.FORWARD,
                Math.map(value, -250, -1023, 0, 255))
            MiniCar.motor(Motorlist.M2,
                Direction1.FORWARD,
                Math.map(value, -250, -1023, 0, 255))
        elif value > 250:
            MiniCar.motor(Motorlist.M1,
                Direction1.BACKWARD,
                Math.map(value, 250, 1023, 0, 255))
            MiniCar.motor(Motorlist.M2,
                Direction1.BACKWARD,
                Math.map(value, 250, 1023, 0, 255))
radio.on_received_value(on_received_value)

radio.set_group(22)
radio.set_transmit_power(7)
basic.show_icon(IconNames.DIAMOND)
led_flip = True
motor_a = 0
motor_a_forward = 0
motor_b = 0
motor_b_forward = 0

def on_every_interval():
    global led_flip
    led_flip = not (led_flip)
    if led_flip:
        MiniCar.led_rgb(LED_rgb_L_R.LED_L, LED_color.RED1)
        MiniCar.led_rgb(LED_rgb_L_R.LED_R, LED_color.BLUE1)
        basic.show_icon(IconNames.SMALL_DIAMOND)
    else:
        MiniCar.led_rgb(LED_rgb_L_R.LED_L, LED_color.BLUE1)
        MiniCar.led_rgb(LED_rgb_L_R.LED_R, LED_color.RED1)
        basic.show_icon(IconNames.DIAMOND)
loops.every_interval(1000, on_every_interval)
