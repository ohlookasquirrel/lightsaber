import colors
import mode
import sound


class State:
    def __init__(self, initial_mode=mode.OFF, initial_color=colors.BLUE):
        self.mode = initial_mode
        self.idle_color = colors.calculate_idle_color(initial_color)
        self.color = initial_color
        self.flash_color = colors.WHITE
        self.mode_selector = mode.SelectableModesItr()
        self.sounds = sound.Lightsaber()

    def __eq__(self, other):
        return self.mode == other.mode \
               and self.idle_color == other.idle_color \
               and self.color == other.color \
               and self.flash_color == other.flash_color \
               and self.mode_selector.current() == other.mode_selector.current()

    def __copy__(self, initial_mode=None, initial_color=None, new_selectable_mode: mode.SelectableMode = None):
        if initial_mode is not None:
            self.mode = initial_mode
        elif initial_color is not None:
            self.idle_color = colors.calculate_idle_color(initial_color)
            self.color = initial_color
            self.flash_color = colors.WHITE
        elif new_selectable_mode is not None:
            self.mode_selector = mode.SelectableModesItr(initial_current=new_selectable_mode)

        return self
