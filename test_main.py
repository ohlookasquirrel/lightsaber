import sys
from unittest.mock import MagicMock

import mode

sys.modules['neopixel'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['pulseio'] = MagicMock()
sys.modules['adafruit_lis3dh'] = MagicMock()
sys.modules['audioio'] = MagicMock()
state_mock = MagicMock()
sys.modules['state'] = state_mock
from state_manager import StateManager
import main


def test_has_hardware():
    assert(main.Hardware is not None)


def test_initializes_state_to_off_mode():
    assert(main.StateManager is not None)


def test_evaluate_powers_on_lightsaber():
    state = StateManager(mode.POWERING_ON)
    hardware = MagicMock()
    main.Saber = MagicMock()
    state = main.evaluate(state, hardware)
    assert state.mode == mode.ON
    main.Saber.power_on.assert_called_with()
