import mode
from Hardware import Hardware
from state_manager import StateManager


class Saber:
    def power_on(self):
        return "powered dog"

def main():
    something = ""


def evaluate(state: StateManager, hardware: Hardware) -> StateManager:
    saber = Saber()
    saber.power_on()
    return StateManager(mode.ON)


if __name__ == '__main__':
    main()
