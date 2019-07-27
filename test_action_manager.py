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


def test_execute_action_turns_on_lightsaber():
    state = State(initial_mode=mode.OFF)
    action = Action(action_manager.POWER_ON)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, state)

    assert returned_state.mode == mode.ON
    action_manager.saber.power.assert_called_with(hardware.strip,
                                                  speaker_mock,
                                                  'on',
                                                  1.0,
                                                  False,
                                                  colors.BLUE)
    action_manager.sound.play_wav.assert_called_with('idle', speaker_mock, loop=True)


def test_execute_action_turns_off_lightsaber():
    state = State(initial_mode=mode.ON)
    action = Action(action_manager.POWER_OFF)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, state)

    assert returned_state.mode == mode.OFF
    action_manager.saber.power.assert_called_with(hardware.strip,
                                                  speaker_mock,
                                                  'off',
                                                  1.0,
                                                  True,
                                                  colors.BLUE)


def test_execute_action_stays_on_if_action_is_none():
    state = State(initial_mode=mode.ON)
    action = Action(action_manager.NONE)
    hardware = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, state)

    assert returned_state.mode == mode.ON


def test_execute_action_stays_off_if_action_is_none():
    state = State(initial_mode=mode.OFF)
    action = Action(action_manager.NONE)
    hardware = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, state)

    assert returned_state.mode == mode.OFF
