import sys
from unittest.mock import MagicMock, call

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


def test_swing_action_plays_sound():
    state = State(initial_mode=mode.ON, initial_color=colors.GREEN)
    state.sounds.swing = lambda: 'swingblah'
    state.sounds.idle = lambda: 'idleblah'
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.swing(hardware, state)

    play_clash_call = call('swingblah', speaker_mock)
    play_idle_call = call('idleblah', speaker_mock, loop=True, override_current_sound=False)
    actions.sound.play_wav.assert_has_calls([play_clash_call, play_idle_call])


def test_swing_action_swells_light():
    state = State(initial_mode=mode.ON, initial_color=colors.GREEN)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.swing(hardware, state)

    actions.saber.swell.assert_called_with(hardware.strip, state.idle_color, state.color)
