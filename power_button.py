class PowerButton:

    def __init__(self, enable, switch, red_led, green_led, blue_led):
        self.enable = enable
        self.switch = switch
        self.red_led = red_led
        self.blue_led = blue_led
        self.green_led = green_led

    def set_color(self, color):
        self.red_led.duty_cycle = int(color[0] * 65536 / 256)
        self.green_led.duty_cycle = int(color[1] * 65536 / 256)
        self.blue_led.duty_cycle = int(color[2] * 65536 / 256)

    def pressed(self):
        return not self.switch.value

    def power_on(self):
        self.enable.value = True

    def power_off(self):
        self.enable.value = False
