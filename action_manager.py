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
    return previous_state.__copy__()
