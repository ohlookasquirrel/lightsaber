PURPLE = (120, 0, 200)
NAVY = (0, 0, 128)
BLUE = (0, 0, 255)
CYAN = (0, 100, 255)
CONSULAR_GREEN = (0, 255, 0)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 200)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

ALL_COLORS = [PURPLE, NAVY, BLUE, CYAN, CONSULAR_GREEN, GREEN, YELLOW, PINK, ORANGE, RED, WHITE]


def calculate_idle_color(color):
    # "Idle" color is 1/4 brightness, "swinging" color is full brightness...
    brightness = 4
    return int(color[0] / brightness), int(color[1] / brightness), int(color[2] / brightness)
