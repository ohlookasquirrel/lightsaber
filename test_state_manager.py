import sys
from unittest.mock import MagicMock, PropertyMock

sys.modules['neopixel'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['pulseio'] = MagicMock()
sys.modules['adafruit_lis3dh'] = MagicMock()
sys.modules['audioio'] = MagicMock()
import mode
import action_manager
from state import State
import state_manager


def test_state_initializes_with_a_mode_of_off():
    state = State()
    assert(state.mode == mode.OFF)


def test_get_action_returns_no_op_when_button_not_pressed_and_is_off():
    state = State(mode.OFF)
    hardware = MagicMock()
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed.return_value = False
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.NONE


def test_get_action_returns_no_op_when_button_not_pressed_and_is_on():
    state = State(mode.ON)
    hardware = MagicMock()
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed.return_value = False
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.NONE


def test_get_action_returns_power_on_action_when_button_released_and_is_off():
    state = State(mode.OFF)
    hardware = MagicMock()
    state_manager.seconds_button_was_pressed = lambda x: 0.123

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.POWER_ON


def test_get_action_returns_power_off_action_when_button_released_and_is_on():
    state = State(mode.ON)
    hardware = MagicMock()
    state_manager.seconds_button_was_pressed = lambda x: 0.123

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.POWER_OFF


def test_get_action_returns_clash_when_accelerometer_crosses_clash_threshold():
    state = State(mode.ON)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()

    state_manager.CLASH_THRESHOLD = 450
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(15, 0, 15))

    state_manager.seconds_button_was_pressed = lambda x: 0

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.CLASH


def test_get_action_returns_swing_when_accelerometer_crosses_swing_threshold():
    state = State(mode.ON)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()

    state_manager.CLASH_THRESHOLD = 600
    state_manager.SWING_THRESHOLD = 200
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(10, 654, 10))
    state_manager.seconds_button_was_pressed = lambda x: 0

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.SWING


def test_get_action_returns_mode_select_when_button_held_for_four_seconds():
    state = State(initial_mode=mode.ON)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()

    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))
    state_manager.seconds_button_was_pressed = lambda x: 4

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.MODE_SELECT


def test_get_action_selects_next_mode():
    state = State(initial_mode=mode.MODE_SELECT)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()

    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))
    state_manager.seconds_button_was_pressed = lambda x: 1

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.MODE_NEXT


def test_get_action_activates_selected_mode_on_long_press():
    state = State(initial_mode=mode.MODE_SELECT)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()

    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))
    state_manager.seconds_button_was_pressed = lambda x: 4

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.ACTIVATE_SELECTED_MODE


def test_get_action_button_press_changes_to_next_color_in_color_change_mode():
    state = State(initial_mode=mode.COLOR_CHANGE)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))
    state_manager.seconds_button_was_pressed = lambda x: 1

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.NEXT_COLOR


def test_get_action_returns_activate_color_when_button_held_in_color_change_mode():
    state = State(initial_mode=mode.COLOR_CHANGE)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(1, 1, 1))
    state_manager.seconds_button_was_pressed = lambda x: 4

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.ACTIVATE_COLOR



