import mode
from Hardware import Hardware


class StateManager:
    def __init__(self, initial_mode=mode.OFF):
        self.mode = initial_mode


def sync_with_hardware(previous_state: StateManager, hardware: Hardware) -> StateManager:
    if hardware.powerButton.pressed():
        if previous_state.mode == mode.OFF:
            return StateManager(mode.POWERING_ON)
        else:
            return StateManager(mode.POWERING_OFF)

