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


def test_clash_action_flashes_light():
    state = State(initial_mode=mode.ON, initial_color=colors.PURPLE)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.clash(hardware, state)

    actions.saber.flash.assert_called_with(hardware.strip, colors.WHITE, state.idle_color, num_of_flashes=1)


def test_clash_action_plays_sound():
    state = State(initial_mode=mode.ON, initial_color=colors.PURPLE)
    state.sounds.idle = lambda: 'idleblah'
    state.sounds.clash = lambda: 'clashblah'
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.clash(hardware, state)

    play_clash_call = call('clashblah', speaker_mock)
    play_idle_call = call('idleblah', speaker_mock, loop=True, override_current_sound=False)
    actions.sound.play_wav.assert_has_calls([play_clash_call, play_idle_call])
