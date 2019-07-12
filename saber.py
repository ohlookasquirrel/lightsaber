
import colors
import gc
import time
import math
import sound

# 132 LED's on zero indexed array
NUM_PIXELS = 131

def mix(color_1, color_2, weight_2):
    """
    Blend between two colors with a given ratio.
    @param color_1:  first color, as an (r,g,b) tuple
    @param color_2:  second color, as an (r,g,b) tuple
    @param weight_2: Blend weight (ratio) of second color, 0.0 to 1.0
    @return: (r,g,b) tuple, blended color
    """
    if weight_2 < 0.0:
        weight_2 = 0.0
    elif weight_2 > 1.0:
        weight_2 = 1.0
    weight_1 = 1.0 - weight_2
    return (int(color_1[0] * weight_1 + color_2[0] * weight_2),
            int(color_1[1] * weight_1 + color_2[1] * weight_2),
            int(color_1[2] * weight_1 + color_2[2] * weight_2))


def off(strip, lower=0, upper=NUM_PIXELS):
    strip[lower:upper] = [0] * (upper-lower)
    strip.show()


def on(strip, lower=0, upper=NUM_PIXELS, color=colors.BLUE):
    for i in range(lower, upper):
        if i <= 5:
            strip[i] = color
        elif 5 < i <= 10:
            strip[i] = colors.WHITE
        elif 11 <= i < 30:
            strip[i] = mix(color, colors.WHITE, 0.5)
        else:
            strip[i] = color
    strip.show()


def power(strip, speaker, sound_name, duration, reverse, color):
    if reverse:
        prev = NUM_PIXELS
    else:
        prev = 0
    gc.collect()                   # Tidy up RAM now so animation's smoother
    start_time = time.monotonic()  # Save audio start time
    sound.play_wav(sound_name, speaker)
    while True:
        elapsed = time.monotonic() - start_time  # Time spent playing sound
        if elapsed > duration:                   # Past sound duration?
            break                                # Stop animating
        fraction = elapsed / duration            # Animation time, 0.0 to 1.0
        if reverse:
            fraction = 1.0 - fraction            # 1.0 to 0.0 if reverse
        fraction = math.pow(fraction, 0.5)       # Apply nonlinear curve
        threshold = int(NUM_PIXELS * fraction + 0.5)
        num = threshold - prev # Number of pixels to light on this pass
        if num != 0:
            if reverse:
                off(strip, lower=threshold, upper=prev)
            else:
                on(strip, lower=prev, upper=threshold, color=color)

            # NeoPixel writes throw off time.monotonic() ever so slightly
            # because interrupts are disabled during the transfer.
            # We can compensate somewhat by adjusting the start time
            # back by 30 microseconds per pixel.
            start_time -= NUM_PIXELS * 0.00003
            prev = threshold

    if reverse:
        off(strip)
    else:
        on(strip, lower=0, upper=NUM_PIXELS, color=color)


def flash(strip, color):
    for i in range(5):
        strip.fill(color)
        strip.show()
        time.sleep(0.01)
        strip.fill(0)
        strip.show()
        time.sleep(0.01)
    strip.fill(color)
    strip.show()



