import Hardware
import colors
import mode
from state import State
import saber
import sound
POWER_ON = "POWER_ON"
NONE = "NONE"
POWER_OFF = "POWER_OFF"
CLASH = "CLASH"
SWING = "SWING"


def execute_action_on_hardware(action, hardware: Hardware, previous_state: State) -> State:
    if action.name == POWER_ON:
        hardware.powerButton.power_on()
        saber.power(hardware.strip, hardware.speaker, 'on', 1.0, False, previous_state.idle_color)
        sound.play_wav('idle', hardware.speaker, loop=True, override_current_sound=False)
        return State(initial_mode=mode.ON, initial_color=previous_state.color)
    elif action.name == POWER_OFF:
        saber.power(hardware.strip, hardware.speaker, 'off', 1.0, True, previous_state.idle_color)
        hardware.powerButton.power_off()
        return State(initial_mode=mode.OFF, initial_color=previous_state.color)
    elif action.name == CLASH:
        sound.play_wav('clash', hardware.speaker)
        saber.flash(hardware.strip, colors.WHITE, previous_state.idle_color, num_of_flashes=1)
        sound.play_wav('idle', hardware.speaker, loop=True, override_current_sound=False)
        return State(initial_mode=mode.ON, initial_color=previous_state.color)
    elif action.name == SWING:
        sound.play_wav('swing', hardware.speaker)
        saber.swell(hardware.strip, previous_state.idle_color, previous_state.color)
        sound.play_wav('idle', hardware.speaker, loop=True, override_current_sound=False)
        return State(initial_mode=mode.ON, initial_color=previous_state.color)
    else:
        return previous_state.__copy__()





