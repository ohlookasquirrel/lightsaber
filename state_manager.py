import actions
import colors
from Hardware import Hardware
import time
import mode
from state import State
from action import Action
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

    elif seconds_button_was_held_for > 0 and state.mode == mode.OFF:
        actions.power_on(hardware, state)
        return state.__copy__(initial_mode=mode.ON)

    elif seconds_button_was_held_for > 0 and state.mode == mode.ON:
        actions.power_off(hardware, state)
        return state.__copy__(initial_mode=mode.OFF)

    elif acceleration_total(hardware) >= CLASH_THRESHOLD:
        actions.clash(hardware, state)
        return state.__copy__()

    elif acceleration_total(hardware) >= SWING_THRESHOLD:
        actions.swing(hardware, state)
        return state.__copy__()

    elif seconds_button_was_held_for > 0 and state.mode == mode.COLOR_CHANGE:
        actions.next_color(hardware, state)
        return state.__copy__(initial_color=colors.next_color(state.color))

    elif state.mode == mode.ON and not hardware.speaker.audio.playing:
        sound.play_wav(state.sounds.idle(), hardware.speaker)
        return state.__copy__()
    else:
        return Action()


def acceleration_total(hardware):
    x, y, z = hardware.accelerometer.acceleration                            # Read accelerometer
    return x * x + z * z
