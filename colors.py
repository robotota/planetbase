import platform

color = None
if platform.system() == "Linux":
    def color_real(attr, bg, fg=None):
        if fg is None:
            fg = "49"
        return chr(16 + 11) + "["+str(attr) + ";" + str(bg) + ";" +str(fg) + "m"
    color = color_real
else:
    def color_fake(attr, bg, fg=None):
        return ""
    color = color_fake        

GRAY = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN= 36
WHITE = 37
NORMAL = 38

    
USUAL = 0
BRIGHT = 1
DIM = 2
UNDERLINE = 4
STRIKE = 9

RESET = color(USUAL, NORMAL)


def term(what):
    return color(USUAL, GREEN) + what+ RESET


def red(what):
    return color(USUAL, RED) + what + RESET


def green(what):
    return color(USUAL, GREEN) + what+ RESET        

