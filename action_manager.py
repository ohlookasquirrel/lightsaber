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
MODE_SELECT = "MODE_SELECT"
MODE_NEXT = "MODE_NEXT"
ACTIVATE_SELECTED_MODE = "ACTIVATE_SELECTED_MODE"
NEXT_COLOR = "NEXT_COLOR"
ACTIVATE_COLOR = "ACTIVATE_COLOR"


def execute_action_on_hardware(action, hardware: Hardware, previous_state: State) -> State:
    if action.name == MODE_SELECT:
        if previous_state.mode != mode.MODE_SELECT:
            sound.play_wav('wow1', hardware.speaker)
            while hardware.powerButton.pressed():  # Wait for button to be released
                pass
        new_state = previous_state.__copy__(initial_mode=mode.MODE_SELECT)
        saber.display_mode_select(hardware.strip, new_state.mode_selector)
        return new_state
    elif action.name == MODE_NEXT:
        new_state = previous_state.__copy__()
        new_state.mode_selector.next()
        return new_state
    elif action.name == ACTIVATE_SELECTED_MODE and previous_state.mode_selector.current().name == 'LIGHTSABER':
        power_on(hardware, previous_state.idle_color, previous_state)
        return State(initial_mode=mode.ON, initial_color=previous_state.color)
    elif action.name == ACTIVATE_SELECTED_MODE and previous_state.mode_selector.current().name == 'COLOR_SELECT':
        saber.on(hardware.strip, color=colors.ALL_COLORS[0])
        return State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.ALL_COLORS[0])
    elif action.name == NEXT_COLOR:
        next_color = colors.next_color(previous_state.color)
        saber.on(hardware.strip, color=next_color)
        return previous_state.__copy__(initial_color=next_color)
    elif action.name == ACTIVATE_COLOR:
        power_on(hardware, previous_state.idle_color, previous_state)
        return previous_state.__copy__(initial_mode=mode.ON)
    else:
        return previous_state.__copy__()


def power_on(hardware, color, state):
    hardware.powerButton.power_on()
    saber.power(hardware.strip, hardware.speaker, state.sounds.on(), 1.0, False, color)
    sound.play_wav(state.sounds.idle(), hardware.speaker, loop=True, override_current_sound=False)





