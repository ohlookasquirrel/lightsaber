import colors
import mode
from Hardware import Hardware
from action import Action
from state import State
import state_manager
import action_manager
import saber


def main():
    state = State(initial_mode=mode.OFF, initial_color=colors.BLUE)
    hardware = Hardware(132)
    saber.off(hardware.strip)
    hardware.powerButton.set_color(state.color)
    while True:
        state = run(state, hardware)


def run(state: State, hardware: Hardware) -> State:
    action = state_manager.get_action(state, hardware)
    if isinstance(action, Action):
        return action_manager.execute_action_on_hardware(action, hardware, previous_state=state)
    else:
        return action  # TODO intermediary fix inbetween refactor. This is a state now.


if __name__ == '__main__':
    main()
