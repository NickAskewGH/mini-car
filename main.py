def on_received_value(name, value):
    if name == "x":
        pass
radio.on_received_value(on_received_value)

led_flip = 0
radio.set_group(22)
basic.show_icon(IconNames.DIAMOND)
bool_store = True

def on_every_interval():
    if Math.random_boolean():
        basic.show_icon(IconNames.SMALL_DIAMOND)
    else:
        basic.show_icon(IconNames.DIAMOND)
loops.every_interval(1000, on_every_interval)

def on_every_interval2():
    global led_flip
    led_flip = 0
    if Math.random_boolean():
        MiniCar.led_rgb(LED_rgb_L_R.LED_L, LED_color.RED1)
        MiniCar.led_rgb(LED_rgb_L_R.LED_R, LED_color.RED1)
    else:
        MiniCar.led_rgb(LED_rgb_L_R.LED_L, LED_color.BLUE1)
        MiniCar.led_rgb(LED_rgb_L_R.LED_R, LED_color.BLUE1)
loops.every_interval(1000, on_every_interval2)

def on_every_interval3():
    if Math.random_boolean():
        MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 51)
        MiniCar.motor(Motorlist.M2, Direction1.FORWARD, 50)
    else:
        MiniCar.motor(Motorlist.M1, Direction1.BACKWARD, 50)
        MiniCar.motor(Motorlist.M2, Direction1.BACKWARD, 50)
loops.every_interval(1000, on_every_interval3)

def on_forever():
    pass
basic.forever(on_forever)
