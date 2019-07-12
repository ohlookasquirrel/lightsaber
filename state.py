import mode


class State:
    def __init__(self, initial_mode=mode.OFF):
        self.mode = initial_mode

    def __eq__(self, other):
        return self.mode == other.mode


