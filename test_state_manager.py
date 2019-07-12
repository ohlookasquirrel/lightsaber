import sys
from unittest.mock import MagicMock

# sys.modules['neopixel'] = MagicMock()
# sys.modules['board'] = MagicMock()
# sys.modules['digitalio'] = MagicMock()
# sys.modules['busio'] = MagicMock()
# sys.modules['pulseio'] = MagicMock()
# sys.modules['adafruit_lis3dh'] = MagicMock()
# sys.modules['audioio'] = MagicMock()
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
    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.NONE


def test_get_action_returns_power_on_action_when_button_released_and_is_off():
    state = State(mode.OFF)
    hardware = MagicMock()
    state_manager.seconds_buttons_was_pressed = lambda x: 0.123

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.POWER_ON


def test_get_action_returns_power_off_action_when_button_released_and_is_on():
    state = State(mode.ON)
    hardware = MagicMock()
    state_manager.seconds_buttons_was_pressed = lambda x: 0.123

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.POWER_OFF





