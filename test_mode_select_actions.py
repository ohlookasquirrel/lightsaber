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


def test_mode_select_action_presents_mode_select():
    state = State(initial_mode=mode.OFF, initial_color=colors.ORANGE)
    hardware = Hardware(30)
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed = MagicMock(return_value=False)    # Code needs to make sure the button is released
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.mode_select(hardware, state)

    actions.saber.display_mode_select.assert_called_with(hardware.strip, state.mode_selector)


def test_mode_select_action_plays_wow():
    state = State(initial_mode=mode.OFF, initial_color=colors.ORANGE)

    hardware = Hardware(30)
    hardware.powerButton.pressed = MagicMock(return_value=False)  # Code needs to make sure the button is released
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.mode_select(hardware, state)

    actions.sound.play_wav.assert_called_with('wow1', speaker_mock)


def test_execute_action_activates_color_change_mode():
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.GREEN)
    state.mode_selector.next()  # select color change mode TODO improve this

    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.activate_color_change_mode(hardware)

    actions.saber.on(hardware.strip, color=colors.ALL_COLORS[0])
