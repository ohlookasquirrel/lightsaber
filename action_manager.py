import Hardware
import colors
import mode
from state import State
import saber
import sound
POWER_ON = "POWER_ON"
NONE = "NONE"
POWER_OFF = "POWER_OFF"


def execute_action_on_hardware(action, hardware: Hardware, previous_state) -> State:
    if action.name == POWER_ON:
        hardware.powerButton.power_on()
        saber.power(hardware.strip, hardware.speaker, 'on', 1.0, False, colors.BLUE)
        sound.play_wav('idle', hardware.speaker, loop=True)
        return State(initial_mode=mode.ON)
    elif action.name == POWER_OFF:
        saber.power(hardware.strip, hardware.speaker, 'off', 1.0, True, colors.BLUE)
        hardware.powerButton.power_off()
        return State(initial_mode=mode.OFF)
    else:
        return State(initial_mode=previous_state.mode)





