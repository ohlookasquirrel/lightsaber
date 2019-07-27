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

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.POWER_ON


def test_get_action_returns_power_off_action_when_button_released_and_is_on():
    state = State(mode.ON)
    hardware = MagicMock()

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.POWER_OFF


def test_get_action_returns_clash_when_accelerometer_crosses_clash_threshold():
    state = State(mode.ON)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()
    hardware.powerButton.pressed.return_value = False

    state_manager.CLASH_THRESHOLD = 450
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(15, 0, 15))

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.CLASH


def test_get_action_returns_swing_when_accelerometer_crosses_swing_threshold():
    state = State(mode.ON)
    hardware = MagicMock()
    hardware.accelerometer = MagicMock()
    hardware.powerButton.pressed.return_value = False

    state_manager.CLASH_THRESHOLD = 600
    state_manager.SWING_THRESHOLD = 200
    type(hardware.accelerometer).acceleration = PropertyMock(return_value=(10, 654, 10))

    action_result = state_manager.get_action(state, hardware)

    assert action_result.name == action_manager.SWING



