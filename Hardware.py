import neopixel
import board
import pulseio
from digitalio import DigitalInOut, Direction, Pull
import busio
import adafruit_lis3dh
import audioio
from speaker import Speaker
from power_button import PowerButton


SPEAKER_PIN = board.A0
NEOPIXEL_PIN = board.D5
SWITCH_PIN = board.D9
POWER_PIN = board.D10


class Hardware:
    def __init__(self, number_of_pixels):
        self.strip = neopixel.NeoPixel(NEOPIXEL_PIN, number_of_pixels, brightness=1, auto_write=False)

        enable = DigitalInOut(POWER_PIN)
        enable.direction = Direction.OUTPUT
        enable.value = False
        switch = DigitalInOut(SWITCH_PIN)
        switch.direction = Direction.INPUT
        switch.pull = Pull.UP

        red_led = pulseio.PWMOut(board.D11, duty_cycle=0, frequency=20000)
        green_led = pulseio.PWMOut(board.D12, duty_cycle=0, frequency=20000)
        blue_led = pulseio.PWMOut(board.D13, duty_cycle=0, frequency=20000)

        self.powerButton = PowerButton(enable, switch, red_led, green_led, blue_led)

        # Set up accelerometer on I2C bus, 4G range:
        i2c = busio.I2C(board.SCL, board.SDA)
        accel = adafruit_lis3dh.LIS3DH_I2C(i2c)
        accel.range = adafruit_lis3dh.RANGE_4_G
        self.accelerometer = accel

        self.speaker = Speaker(audioio.AudioOut(SPEAKER_PIN), audioio)
