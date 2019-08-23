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


def test_power_on_action_turns_on_lightsaber():
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()
    state = State(initial_mode=mode.OFF, initial_color=colors.CONSULAR_GREEN)
    state.sounds.on = lambda: 'onblah'
    state.sounds.idle = lambda: 'idleblah'

    actions.power_on(hardware, state)

    actions.saber.power.assert_called_with(hardware.strip,
                                                  speaker_mock,
                                                  'onblah',
                                                  1.0,
                                                  False,
                                                  state.idle_color)
    actions.sound.play_wav.assert_called_with('idleblah', speaker_mock, override_current_sound=False)
