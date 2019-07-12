from Hardware import Hardware
import time
import mode
from state import State
from action import Action
import action_manager


def sync_with_hardware(state: State, hardware):
    if state.mode == mode.ON:
        hardware.saber.on(hardware.strip, lower=0, upper=hardware.NUM_PIXELS)
    else:
        hardware.saber.off(hardware.strip, lower=0, upper=hardware.NUM_PIXELS)


def seconds_buttons_was_pressed(hardware):
    if not hardware.powerButton.pressed():
        return 0  # To avoid small execution time differences showing up as a press

    time_button_was_pressed = time.monotonic()
    while hardware.powerButton.pressed():
        pass
    return time_button_was_pressed - time.monotonic()


def get_action(state: State, hardware: Hardware) -> Action:
    if seconds_buttons_was_pressed(hardware) > 0:
        return Action(action_manager.POWER_ON) if state.mode == mode.OFF else Action(action_manager.POWER_OFF)
    else:
        return Action()

