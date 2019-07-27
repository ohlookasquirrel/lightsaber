from Hardware import Hardware
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

    elif acceleration_total(hardware) >= CLASH_THRESHOLD:
        return Action(action_manager.CLASH)

    elif acceleration_total(hardware) >= SWING_THRESHOLD:
        return Action(action_manager.SWING)

    else:
        return Action()


def acceleration_total(hardware):
    x, y, z = hardware.accelerometer.acceleration                            # Read accelerometer
    return x * x + z * z
