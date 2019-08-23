import sys
from unittest.mock import MagicMock

neopixel_mock = MagicMock()
sys.modules['neopixel'] = neopixel_mock
sys.modules['board'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['pulseio'] = MagicMock()
sys.modules['adafruit_lis3dh'] = MagicMock()
audioio_mock = MagicMock()
sys.modules['audioio'] = audioio_mock

from state import State
import colors
import mode
from action import Action
from Hardware import Hardware
import action_manager


def test_execute_action_stays_on_if_action_is_none():
    state = State(mode.ON)
    action = Action(action_manager.NONE)
    hardware = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.ON


def test_execute_action_stays_off_if_action_is_none():
    state = State(mode.OFF)
    action = Action(action_manager.NONE)
    hardware = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.OFF

