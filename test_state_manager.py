import sys
from unittest.mock import MagicMock, PropertyMock

import pytest

import colors
from Hardware import Hardware
from sound import Wowsaber

sys.modules['neopixel'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['pulseio'] = MagicMock()
sys.modules['adafruit_lis3dh'] = MagicMock()
sys.modules['audioio'] = MagicMock()
import mode
from state import State
import state_manager


@pytest.fixture()
def hardware():
    hardware = Hardware(30)
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed.return_value = False
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))
    hardware.speaker = MagicMock()
    hardware.speaker.audio = MagicMock()
    return hardware


def setup_function():
    state_manager.actions = MagicMock()
    state_manager.seconds_button_was_pressed = lambda x: 0


#  TODO move this to main test
def test_state_initializes_with_a_mode_of_off():
    state = State()
    assert(state.mode == mode.OFF)


def test_get_action_returns_no_op_when_button_not_pressed_and_is_off(hardware):
    state = State(mode.OFF)

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state == state


def test_get_action_returns_no_op_when_button_not_pressed_and_is_on(hardware):
    state = State(mode.ON)

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state == state


def test_get_action_calls_power_on_action_when_button_released_and_is_off(hardware):
    state = State(initial_mode=mode.OFF, initial_color=colors.GREEN)
    state_manager.seconds_button_was_pressed = lambda x: 0.123

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.GREEN
    state_manager.actions.power_on.assert_called_with(hardware, state)


def test_get_action_calls_power_off_action_when_button_released_and_is_on(hardware):
    state = State(initial_mode=mode.ON, initial_color=colors.PURPLE)
    state_manager.seconds_button_was_pressed = lambda x: 0.123

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.OFF
    assert returned_state.color == colors.PURPLE
    state_manager.actions.power_off.assert_called_with(hardware, state)


def test_get_action_plays_idle_sound_when_mode_is_on_and_nothing_else_happens(hardware):
    state = State(initial_mode=mode.ON, initial_color=colors.ORANGE)

    type(hardware.speaker.audio).playing = PropertyMock(return_value=False)

    state_manager.sound = MagicMock()

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state == state
    state_manager.sound.play_wav.assert_called_with(state.sounds.idle(), hardware.speaker)

    # Teardown
    import sound as sound_module
    state_manager.sound = sound_module


def test_get_action_calls_clash_when_accelerometer_crosses_clash_threshold(hardware):
    state = State(initial_mode=mode.ON, initial_color=colors.PINK)

    state_manager.CLASH_THRESHOLD = 450
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(15, 0, 15))

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.PINK
    state_manager.actions.clash.assert_called_with(hardware, state)


def test_get_action_calls_swing_when_accelerometer_crosses_swing_threshold(hardware):
    state = State(initial_mode=mode.ON, initial_color=colors.ORANGE)

    state_manager.CLASH_THRESHOLD = 600
    state_manager.SWING_THRESHOLD = 200
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(10, 654, 10))

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state == state
    state_manager.actions.swing.assert_called_with(hardware, state)


def test_get_action_calls_mode_select_when_button_held_for_four_seconds(hardware):
    state = State(initial_mode=mode.ON, initial_color=colors.CYAN)

    state_manager.seconds_button_was_pressed = lambda x: 4

    expected_selected_mode = mode.SelectableModesItr().current()

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.MODE_SELECT
    assert returned_state.color == colors.CYAN
    assert returned_state.mode_selector.current() == expected_selected_mode
    state_manager.actions.mode_select.assert_called_with(hardware, state)


def test_get_action_selects_next_mode(hardware):
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.GREEN)

    state_manager.seconds_button_was_pressed = lambda x: 1

    returned_state = state_manager.get_action(state, hardware)

    expected_selected_mode = mode.SelectableModesItr().next()

    assert returned_state.mode == mode.MODE_SELECT
    assert returned_state.color == colors.GREEN
    assert returned_state.mode_selector.current() == expected_selected_mode
    state_manager.actions.mode_select.assert_called_with(hardware, state)


def test_get_action_activates_lightsaber_mode(hardware):
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.GREEN)
    state_manager.seconds_button_was_pressed = lambda x: 4

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.color == colors.GREEN
    assert returned_state.mode == mode.ON
    state_manager.actions.power_on.assert_called_with(hardware, state)


def test_get_action_activates_color_change_mode(hardware):
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.GREEN)
    state.mode_selector.next()  # select color change mode TODO improve this

    state_manager.seconds_button_was_pressed = lambda x: 4

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.COLOR_CHANGE
    assert returned_state.color == colors.ALL_COLORS[0]
    state_manager.actions.activate_color_change_mode(hardware)


def test_get_action_button_press_changes_to_next_color_in_color_change_mode(hardware):
    state = State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.ALL_COLORS[0])

    state_manager.seconds_button_was_pressed = lambda x: 1

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.COLOR_CHANGE
    assert returned_state.color == colors.ALL_COLORS[1]
    state_manager.actions.next_color.assert_called_with(hardware, state)


def test_get_action_powers_on_with_current_color_when_button_held_in_color_change_mode(hardware):
    state = State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.NAVY)

    state_manager.seconds_button_was_pressed = lambda x: 4

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.NAVY
    state_manager.actions.power_on.assert_called_with(hardware, state)


def test_execute_action_activate_selected_mode_activates_wow_mode(hardware):
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.NAVY)
    state.mode_selector.next()
    state.mode_selector.next()  # Select third mode aka wow mode, TODO this needs improving

    state_manager.seconds_button_was_pressed = lambda x: 4

    returned_state = state_manager.get_action(state, hardware)

    assert returned_state.color == colors.NAVY
    assert returned_state.mode == mode.ON
    assert isinstance(returned_state.sounds, Wowsaber)
    state_manager.actions.power_on.assert_called_with(hardware, state)
