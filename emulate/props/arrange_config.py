import pygame


OLED = {"WIDTH": 128, "HEIGHT": 64, "CASE_Y_OFF": 10, "COLOR": pygame.Color("green")}

CASE = {"WIDTH": 150, "HEIGHT": 180, "COLOR": pygame.Color("gray")}

BUTTONS_CASE_Y_OFFSET = 130

DPAD = {
    "SHORT_LENGTH": 15,
    "LONG_LENGTH": 21,
    "CASE_LEFT_X_OFF": 40,
    "CASE_Y_OFF": BUTTONS_CASE_Y_OFFSET,
    "CENTER_OFFSET": 8,
    "COLOR_DOWN": pygame.Color("maroon"),
    "COLOR_UP": pygame.Color("pink"),
}

SBUT = {
    "CASE_RIGHT_X_OFF": 35,
    "CASE_Y_OFF": BUTTONS_CASE_Y_OFFSET,
    "CENTER_OFFSET": 10,
    "RADIUS": 27,
    "B_NUDGE": -10,
    "COLOR_DOWN": pygame.Color("cyan"),
    "COLOR_UP": pygame.Color("blue"),
}
