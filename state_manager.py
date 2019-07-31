from Hardware import Hardware
import time
import mode
from state import State
from action import Action
import action_manager


CLASH_THRESHOLD = 350
SWING_THRESHOLD = 200
# TODO remove prints


def seconds_button_was_pressed(hardware):
    if not hardware.powerButton.pressed():
        return 0  # To avoid small execution time differences showing up as a press

    time_button_was_pressed = time.monotonic()
    while hardware.powerButton.pressed():
        if time.monotonic() - time_button_was_pressed >= 4:
            break  # Break out for mode select
        pass
    x = time.monotonic() - time_button_was_pressed
    print("Button was pressed for %s seconds" % x)
    return x


def get_action(state: State, hardware: Hardware) -> Action:
    seconds_button_was_held_for = seconds_button_was_pressed(hardware)

    if seconds_button_was_held_for >= 4 and state.mode == mode.COLOR_CHANGE:
        return Action(action_manager.ACTIVATE_COLOR)

    elif seconds_button_was_held_for >= 4 and state.mode == mode.MODE_SELECT:
        return Action(action_manager.ACTIVATE_SELECTED_MODE)

    elif seconds_button_was_held_for >= 4:
        return Action(action_manager.MODE_SELECT)

    elif seconds_button_was_held_for > 0 and state.mode == mode.MODE_SELECT:
        return Action(action_manager.MODE_NEXT)

    elif state.mode == mode.MODE_SELECT:
        return Action(action_manager.MODE_SELECT)

    elif seconds_button_was_held_for > 0 and state.mode == mode.OFF:
        return Action(action_manager.POWER_ON)

    elif seconds_button_was_held_for > 0 and state.mode == mode.ON:
        return Action(action_manager.POWER_OFF)

    elif acceleration_total(hardware) >= CLASH_THRESHOLD:
        return Action(action_manager.CLASH)

    elif acceleration_total(hardware) >= SWING_THRESHOLD:
        return Action(action_manager.SWING)

    elif seconds_button_was_held_for > 0 and state.mode == mode.COLOR_CHANGE:
        return Action(action_manager.NEXT_COLOR)

    else:
        return Action()


def acceleration_total(hardware):
    x, y, z = hardware.accelerometer.acceleration                            # Read accelerometer
    return x * x + z * z
