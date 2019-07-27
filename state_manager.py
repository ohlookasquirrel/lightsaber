from Hardware import Hardware
import time
import mode
from state import State
from action import Action
import action_manager


CLASH_THRESHOLD = 350
SWING_THRESHOLD = 200
# TODO remove prints


def get_action(state: State, hardware: Hardware) -> Action:
    if hardware.powerButton.pressed() and state.mode == mode.OFF:
        return Action(action_manager.POWER_ON)

    elif hardware.powerButton.pressed() and state.mode == mode.ON:
        return Action(action_manager.POWER_OFF)

    else:
        return Action()