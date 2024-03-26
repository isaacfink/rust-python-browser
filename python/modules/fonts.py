import tkinter.font as tkFont
import tkinter as tk


FONTS = {}


def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkFont.Font(size=size, weight=weight, slant=slant)
        label = tk.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]
