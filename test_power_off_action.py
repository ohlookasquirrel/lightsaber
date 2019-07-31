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

from Hardware import Hardware
from state import State
import colors
import mode
import actions


def test_power_off_action_turns_off_lightsaber():
    state = State(initial_mode=mode.ON, initial_color=colors.CYAN)
    state.sounds.off = lambda: 'offblah'
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.power_off(hardware, state)

    actions.saber.power.assert_called_with(hardware.strip, speaker_mock, 'offblah', 1.0, True, state.idle_color)
