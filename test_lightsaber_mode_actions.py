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
    actions.sound.play_wav.assert_called_with('idleblah', speaker_mock, loop=True, override_current_sound=False)


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


def test_cycle_idle_loop_stops_and_starts_idle_sound():
    state = State(initial_mode=mode.ON, initial_color=colors.ORANGE)
    state.sounds.idle = lambda: 'idleblah'
    hardware = Hardware(30)
    hardware.speaker = MagicMock()
    hardware.speaker.audio = MagicMock()
    actions.saber = MagicMock()
    actions.sound = MagicMock()

    actions.cycle_idle_loop(hardware, state)

    hardware.speaker.audio.stop.assert_called_with()
    actions.sound.play_wav.assert_called_with('idleblah', hardware.speaker, loop=True)
