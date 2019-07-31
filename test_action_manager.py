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


def test_execute_action_moves_to_next_color_on_next_color_action():
    state = State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.ALL_COLORS[0])
    action = Action(action_manager.NEXT_COLOR)

    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.COLOR_CHANGE
    assert returned_state.color == colors.ALL_COLORS[1]
    action_manager.saber.on(hardware.strip, color=colors.ALL_COLORS[1])


def test_execute_action_loops_back_to_first_color_on_next_color_action():
    state = State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.ALL_COLORS[len(colors.ALL_COLORS) - 1])
    action = Action(action_manager.NEXT_COLOR)

    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.COLOR_CHANGE
    assert returned_state.color == colors.ALL_COLORS[0]
    action_manager.saber.on(hardware.strip, color=colors.ALL_COLORS[0])


def test_execute_action_selects_current_color_and_changed_to_lightsaber_mode_on_activate_color():
    state = State(initial_mode=mode.COLOR_CHANGE, initial_color=colors.PURPLE)
    state.sounds.on = lambda: 'onblah'
    state.sounds.idle = lambda: 'idleblah'
    action = Action(action_manager.ACTIVATE_COLOR)

    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.color == colors.PURPLE
    assert returned_state.mode == mode.ON
    action_manager.saber.power.assert_called_with(hardware.strip, speaker_mock, 'onblah', 1.0, False, state.idle_color)
    action_manager.sound.play_wav.assert_called_with('idleblah', speaker_mock, loop=True, override_current_sound=False)


def test_execute_action_activate_selected_mode_activates_wow_mode():
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.PURPLE)
    state.sounds.on = lambda: 'onblah'
    state.sounds.idle = lambda: 'idleblah'
    action = Action(action_manager.ACTIVATE_COLOR)

    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.color == colors.PURPLE
    assert returned_state.mode == mode.ON
    action_manager.saber.power.assert_called_with(hardware.strip, speaker_mock, 'onblah', 1.0, False, state.idle_color)
    action_manager.sound.play_wav.assert_called_with('idleblah', speaker_mock, loop=True, override_current_sound=False)
