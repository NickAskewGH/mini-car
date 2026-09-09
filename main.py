def on_received_value(name, value):
    if name == "x":
        if value < -500:
            MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 0)
            MiniCar.motor(Motorlist.M2, Direction1.FORWARD, 0)
        elif value > 500:
            MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 0)
            MiniCar.motor(Motorlist.M2, Direction1.FORWARD, 0)
        else:
            MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 0)
            MiniCar.motor(Motorlist.M2, Direction1.FORWARD, 0)
    elif name == "y":
        if value < -250:
            MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 0)
            MiniCar.motor(Motorlist.M2, Direction1.FORWARD, 0)
        elif value > 250:
            MiniCar.motor(Motorlist.M1, Direction1.FORWARD, 0)
            MiniCar.motor(Motorlist.M2, Direction1.FORWARD, 0)
radio.on_received_value(on_received_value)

radio.set_group(20)
radio.set_transmit_power(7)
basic.show_icon(IconNames.DIAMOND)
led_flip = True
music.play(music.builtin_playable_sound_effect(soundExpression.slide),
    music.PlaybackMode.IN_BACKGROUND)

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
