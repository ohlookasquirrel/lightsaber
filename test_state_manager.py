from unittest.mock import MagicMock
import mode
from state_manager import StateManager, sync_with_hardware


def test_initializes_with_a_mode_of_off():
    state = StateManager()
    assert(state.mode == mode.OFF)


def test_sync_with_hardware_flags_button_press_from_off_mode():
    state = StateManager()
    hardware = MagicMock()
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed.return_value = True

    new_state = sync_with_hardware(state, hardware)
    assert new_state.mode == mode.POWERING_ON


def test_sync_with_hardware_powers_off_when_button_pressed_from_on():
    state = StateManager(mode.ON)
    hardware = MagicMock()
    hardware.powerButton = MagicMock()
    hardware.powerButton.pressed.return_value = True

    new_state = sync_with_hardware(state, hardware)
    assert new_state.mode == mode.POWERING_OFF


