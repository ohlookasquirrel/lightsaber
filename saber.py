
import colors
import gc
import time
import math
import sound
import mode
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
        elif 11 <= i < 20:
            strip[i] = mix(color, colors.WHITE, 0.02)
        elif 21 <= i < 26:
            strip[i] = mix(color, colors.WHITE, 0.01)
        elif 27 <= i < 30:
            strip[i] = mix(color, colors.WHITE, 0.005)
        else:
            strip[i] = color
    strip.show()


def power(strip, speaker, sound_name, duration, reverse, color):
    if reverse:
        prev = NUM_PIXELS
    else:
        prev = 0
    gc.collect()                                # Tidy up RAM now so animation's smoother
    start_time = time.monotonic()               # Save audio start time
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
        num = threshold - prev                   # Number of pixels to light on this pass
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


def flash(strip, flash_color, return_color, num_of_flashes=5, flash_delay=0.01, lower=0, upper=NUM_PIXELS):
    for i in range(num_of_flashes):
        strip[lower:upper] = [flash_color] * (upper-lower)
        strip.show()
        time.sleep(flash_delay)
        on(strip, color=return_color, lower=lower, upper=upper)
        time.sleep(flash_delay)


def swell(strip, main_color, secondary_color):
    gc.collect()
    on(strip, color=mix(main_color, secondary_color, 0.1))
    on(strip, color=mix(main_color, secondary_color, 0.2))
    on(strip, color=mix(main_color, secondary_color, 0.3))
    on(strip, color=mix(main_color, secondary_color, 0.4))
    on(strip, color=mix(main_color, secondary_color, 0.5))
    on(strip, color=mix(main_color, secondary_color, 0.4))
    on(strip, color=mix(main_color, secondary_color, 0.3))
    on(strip, color=mix(main_color, secondary_color, 0.2))
    on(strip, color=mix(main_color, secondary_color, 0.1))
    on(strip, color=main_color)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow(strip, wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            rc_index = (i * 256 // NUM_PIXELS) + j
            strip[i] = wheel(rc_index & 255)
        strip.show()
        time.sleep(wait)


def display_mode_select(strip, mode_selector: mode.SelectableModesItr):
    for current_mode in mode_selector.selectable_modes:
        strip[current_mode.lower_led_bound:current_mode.upper_led_bound] = \
            [current_mode.color] * (current_mode.upper_led_bound - current_mode.lower_led_bound)

    selected_mode = mode_selector.current()
    strip[selected_mode.lower_led_bound:selected_mode.upper_led_bound] = \
        [colors.WHITE] * (selected_mode.upper_led_bound - selected_mode.lower_led_bound)
    strip.show()

