import actions
import colors
import saber
from Hardware import Hardware
import time
import mode
from state import State
import sound


CLASH_THRESHOLD = 300
SWING_THRESHOLD = 250
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


def evaluate_lightsaber(hardware: Hardware, state: State) -> State:
    new_state = state.__copy__()

    seconds_button_was_held_for = seconds_button_was_pressed(hardware)
    if seconds_button_was_held_for >= 4:
        new_state = new_state.__copy__(initial_mode=mode.MODE_SELECT)

    elif seconds_button_was_held_for > 0 and state.state == mode.OFF:
        actions.power_on(hardware, state)
        new_state.state = mode.ON

    elif seconds_button_was_held_for > 0 and state.state == mode.ON:
        actions.power_off(hardware, state)
        new_state.state = mode.OFF

    elif acceleration_total(hardware) >= CLASH_THRESHOLD:
        actions.clash(hardware, state)

    elif acceleration_total(hardware) >= SWING_THRESHOLD:
        actions.swing(hardware, state)

    elif state.state == mode.ON and time.monotonic() - state.time_since_wav_was_looped >= 4:
        actions.cycle_idle_loop(hardware, state)
        new_state = state.__copy__()
        new_state.time_since_wav_was_looped = time.monotonic()

    return new_state


def evaluate_mode_select(hardware: Hardware, state: State) -> State:
    new_state = state.__copy__()

    return new_state


#  TODO add return type when done with refactor
def get_action(state: State, hardware: Hardware):
    seconds_button_was_held_for = seconds_button_was_pressed(hardware)

    if seconds_button_was_held_for >= 4 and state.mode == mode.COLOR_CHANGE:
        actions.power_on(hardware, state)
        return state.__copy__(initial_mode=mode.ON)

    elif seconds_button_was_held_for >= 4 and state.mode == mode.MODE_SELECT and state.mode_selector.current().name == 'LIGHTSABER':
        actions.power_on(hardware, state)
        return state.__copy__(initial_mode=mode.ON)

    elif seconds_button_was_held_for >= 4 and state.mode == mode.MODE_SELECT and state.mode_selector.current().name == 'COLOR_SELECT':
        actions.activate_color_change_mode(hardware)
        return State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.ALL_COLORS[0])

    elif seconds_button_was_held_for >= 4 and state.mode == mode.MODE_SELECT and state.mode_selector.current().name == 'WOWSABER':
        actions.power_on(hardware, state)
        new_state = state.__copy__(initial_mode=mode.ON)
        new_state.sounds = sound.Wowsaber()
        return new_state

    elif seconds_button_was_held_for >= 4:
        actions.mode_select(hardware, state)
        return state.__copy__(initial_mode=mode.MODE_SELECT)

    elif seconds_button_was_held_for > 0 and state.mode == mode.MODE_SELECT:
        new_state = state.__copy__()
        new_state.mode_selector.next()
        actions.mode_select(hardware, state)
        return new_state

    elif seconds_button_was_held_for > 0 and state.mode == mode.COLOR_CHANGE:
        actions.next_color(hardware, state)
        return state.__copy__(initial_color=colors.next_color(state.color))

    else:
        return state.__copy__()


def acceleration_total(hardware):
    x, y, z = hardware.accelerometer.acceleration                            # Read accelerometer
    return x * x + z * z
