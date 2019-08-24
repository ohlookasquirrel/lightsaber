import colors
import mode
from Hardware import Hardware
from state import State
import state_manager
import saber


def main():
    state = State(initial_mode=mode.LIGHTSABER, initial_color=colors.BLUE)
    hardware = Hardware(132)
    saber.off(hardware.strip)
    hardware.powerButton.set_color(state.color)
    while True:
        state = run(state, hardware)


def run(state: State, hardware: Hardware) -> State:
    if state.mode == mode.LIGHTSABER:
        return state_manager.evaluate_lightsaber(hardware, state)
    else:
        return state_manager.get_action(state, hardware)


if __name__ == '__main__':
    main()
