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

from state import State
import colors
import mode
from action import Action
from Hardware import Hardware
import action_manager


def test_execute_action_turns_on_lightsaber():
    action = Action(action_manager.POWER_ON)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()
    state = State(initial_mode=mode.OFF, initial_color=colors.CONSULAR_GREEN)

    returned_state = action_manager.execute_action_on_hardware(action, hardware, state)

    assert returned_state.mode == mode.ON
    action_manager.saber.power.assert_called_with(hardware.strip,
                                                  speaker_mock,
                                                  'on',
                                                  1.0,
                                                  False,
                                                  state.idle_color)
    action_manager.sound.play_wav.assert_called_with('idle', speaker_mock, loop=True, override_current_sound=False)


def test_execute_action_turns_off_lightsaber():
    state = State(initial_mode=mode.ON, initial_color=colors.CYAN)
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
                                                  state.idle_color)


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


def test_execute_action_flashes_light_on_clash():
    state = State(initial_mode=mode.ON, initial_color=colors.PURPLE)
    action = Action(action_manager.CLASH)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.PURPLE
    action_manager.saber.flash.assert_called_with(hardware.strip,
                                                  colors.WHITE,
                                                  state.idle_color,
                                                  num_of_flashes=1)


def test_execute_action_plays_sound_on_clash():
    state = State(initial_mode=mode.ON, initial_color=colors.PURPLE)
    action = Action(action_manager.CLASH)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.PURPLE
    play_clash_call = call('clash', speaker_mock)
    play_idle_call = call('idle', speaker_mock, loop=True, override_current_sound=False)
    action_manager.sound.play_wav.assert_has_calls([play_clash_call, play_idle_call])


def test_execute_action_plays_sound_on_swing():
    state = State(initial_mode=mode.ON, initial_color=colors.GREEN)
    action = Action(action_manager.SWING)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.GREEN
    play_clash_call = call('swing', speaker_mock)
    play_idle_call = call('idle', speaker_mock, loop=True, override_current_sound=False)
    action_manager.sound.play_wav.assert_has_calls([play_clash_call, play_idle_call])


def test_execute_action_swells_light_on_swing():
    state = State(initial_mode=mode.ON, initial_color=colors.GREEN)
    action = Action(action_manager.SWING)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.ON
    assert returned_state.color == colors.GREEN
    action_manager.saber.swell.assert_called_with(hardware.strip, state.idle_color, state.color)


def test_execute_action_mode_select_presents_mode_select():
    state = State(initial_mode=mode.OFF, initial_color=colors.ORANGE)
    action = Action(action_manager.MODE_SELECT)
    hardware = Hardware(30)
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed = MagicMock(return_value=False)    # Code needs to make sure the button is released
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()
    expected_selected_mode = mode.SelectableModesItr().current()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.MODE_SELECT
    assert returned_state.color == colors.ORANGE
    assert returned_state.mode_selector.current() == expected_selected_mode
    action_manager.saber.display_mode_select.assert_called_with(hardware.strip, state.mode_selector)


def test_execute_action_mode_select_plays_wow():
    state = State(initial_mode=mode.OFF, initial_color=colors.ORANGE)
    expected_selected_mode = state.mode_selector.next()

    action = Action(action_manager.MODE_SELECT)
    hardware = Hardware(30)
    hardware.powerButton.pressed = MagicMock(return_value=False)  # Code needs to make sure the button is released
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.MODE_SELECT
    assert returned_state.color == colors.ORANGE
    assert returned_state.mode_selector.current() == expected_selected_mode
    action_manager.sound.play_wav.assert_called_with('wow1', speaker_mock)


def test_execute_action_select_mode_next_sets_the_next_mode():
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.GREEN)
    expected_selected_mode = mode.SelectableModesItr().next()
    action = Action(action_manager.MODE_NEXT)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.mode == mode.MODE_SELECT
    assert returned_state.color == colors.GREEN
    assert returned_state.mode_selector.current() == expected_selected_mode


def test_execute_action_activates_lightsaber_mode():
    state = State(initial_mode=mode.MODE_SELECT, initial_color=colors.GREEN)
    action = Action(action_manager.ACTIVATE_SELECTED_MODE)
    hardware = Hardware(30)
    speaker_mock = MagicMock()
    hardware.speaker = speaker_mock
    action_manager.saber = MagicMock()
    action_manager.sound = MagicMock()

    returned_state = action_manager.execute_action_on_hardware(action, hardware, previous_state=state)

    assert returned_state.color == colors.GREEN
    assert returned_state.mode == mode.ON
    action_manager.saber.power.assert_called_with(hardware.strip,
                                              speaker_mock,
                                              'on',
                                              1.0,
                                              False,
                                              state.idle_color)
    action_manager.sound.play_wav.assert_called_with('idle', speaker_mock, loop=True, override_current_sound=False)



