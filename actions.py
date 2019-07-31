import colors
import mode
from Hardware import Hardware
from state import State
import saber
import sound


def power_on(hardware: Hardware, state: State):
    hardware.powerButton.power_on()
    saber.power(hardware.strip, hardware.speaker, state.sounds.on(), 1.0, False, state.idle_color)
    sound.play_wav(state.sounds.idle(), hardware.speaker, loop=True, override_current_sound=False)


def power_off(hardware: Hardware, state: State):
    saber.power(hardware.strip, hardware.speaker, state.sounds.off(), 1.0, True, state.idle_color)
    hardware.powerButton.power_off()


def clash(hardware: Hardware, state: State):
    sound.play_wav(state.sounds.clash(), hardware.speaker)
    saber.flash(hardware.strip, colors.WHITE, state.idle_color, num_of_flashes=1)
    sound.play_wav(state.sounds.idle(), hardware.speaker, loop=True, override_current_sound=False)


def swing(hardware: Hardware, state: State):
    sound.play_wav(state.sounds.swing(), hardware.speaker)
    saber.swell(hardware.strip, state.idle_color, state.color)
    sound.play_wav(state.sounds.idle(), hardware.speaker, loop=True, override_current_sound=False)


def mode_select(hardware: Hardware, state: State):
    if state.mode != mode.MODE_SELECT:
        sound.play_wav('wow1', hardware.speaker)
        while hardware.powerButton.pressed():  # Wait for button to be released
            pass
    saber.display_mode_select(hardware.strip, state.mode_selector)


def activate_color_change_mode(hardware: Hardware):
    saber.on(hardware.strip, color=colors.ALL_COLORS[0])
