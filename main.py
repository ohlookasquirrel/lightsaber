import colors
import mode
from Hardware import Hardware
from state import State
import state_manager
import action_manager


def main():
    state = mode.OFF
    hardware = Hardware(132)
    hardware.powerButton.set_color(colors.BLUE)
    while True:
        state = run(state, hardware)


def run(state: State, hardware: Hardware) -> State:
    action = state_manager.get_action(state, hardware)
    return action_manager.execute_action_on_hardware(action, hardware, state)


if __name__ == '__main__':
    main()
