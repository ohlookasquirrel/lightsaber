import colors

OFF = 0
ON = 1
MODE_SELECT = 2
COLOR_CHANGE = 3


class SelectableMode:
    def __init__(self, name: str, color, sound: str):
        self.name = name
        self.color = color
        self.sound = sound
        self.lower_led_bound = 0
        self.upper_led_bound = 0

    def __str__(self):
        return '{name: %s, color: %s, sound: %s, lower_led_bound: %s, upper_led_bound: %s}'\
               % (self.name, self.color, self.sound, self.lower_led_bound, self.upper_led_bound)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name \
            and self.color == other.color \
            and self.sound == other.sound


def generate_selectable_modes():
    selectable_modes = [SelectableMode('LIGHTSABER', colors.BLUE, 'on'),
                        SelectableMode('COLOR_SELECT', colors.ORANGE, 'clash'),
                        SelectableMode('WOWSABER', colors.PURPLE, 'wow1')]
    import saber
    step = saber.NUM_PIXELS // len(selectable_modes)
    lower = 0
    upper = step

    mode_array = []
    for mode in selectable_modes:
        mode.lower_led_bound = lower
        mode.upper_led_bound = upper
        mode_array.append(mode)
        lower = upper
        upper = upper + step

    return mode_array


class SelectableModesItr:
    def __init__(self, initial_current: SelectableMode = None):
        self.selectable_modes = generate_selectable_modes()
        if initial_current is None:
            self.current_mode = self.selectable_modes[0]
        else:
            self.current_mode = initial_current

    def __iter__(self):
        return self

    def current(self) -> SelectableMode:
        return self.current_mode

    def next(self) -> SelectableMode:
        i = self.selectable_modes.index(self.current_mode)
        if i + 1 >= len(self.selectable_modes):
            i = -1
        self.current_mode = self.selectable_modes[i + 1]
        return self.current_mode




