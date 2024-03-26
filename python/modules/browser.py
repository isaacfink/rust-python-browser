import tkinter as tk
import tkinter.font as tkFont
from .html import Tag, Text
from typing import Literal

hstep, vstep = 13, 18


class Browser:
    def __init__(self, lines: list[Tag | Text] = [], width=800, height=600) -> None:
        self.window = tk.Tk()
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()
        self.scroll = 0
        self.scroll_step = 100
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        self.fonts = {
            "times": tkFont.Font(
                family="Times", size=16, weight="bold", slant="italic"
            ),
            "halvetica": tkFont.Font(
                family="Helvetica", size=16, weight="bold", slant="italic"
            ),
        }
        self.display_list = Layout(lines, self.width, self.height).display_list

    def scroll_down(self, event):
        self.scroll += self.scroll_step
        self.draw()

    def scroll_up(self, event):
        self.scroll -= self.scroll_step
        self.draw()

    def draw(self):

        self.canvas.delete("all")
        self.show()

    def start(self):
        tk.mainloop()

    def show(self):
        for x, y, c, f in self.display_list:
            if y > self.scroll + self.height:
                continue
            if y + vstep < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor="nw")


class Layout:
    def __init__(self, tokens: list[Tag | Text], width: int, height: int) -> None:
        self.tokens = tokens
        self.width = width
        self.height = height
        self.style: Literal["roman", "italic"] = "roman"
        self.weight: Literal["normal", "bold"] = "normal"
        self.cursor_x = hstep
        self.cursor_y = vstep
        self.font = tkFont.Font(family="Times", size=16, weight="normal", slant="roman")
        self.display_list: list[tuple[int, int | float, str, tkFont.Font]] = []
        for token in tokens:
            self.tokenize(token)

    def tokenize(self, token: Tag | Text):
        if isinstance(token, Text):
            self.word(token.text)
        elif token.tag == "i":
            self.style = "italic"
        elif token.tag == "b":
            self.weight = "bold"
        elif token.tag == "/i":
            self.style = "roman"
        elif token.tag == "/b":
            self.weight = "normal"

    def word(self, word: str):
        w = self.font.measure(word)
        wordFont = tkFont.Font(
            family=self.font.cget("family"),
            size=self.font.cget("size"),
            weight=self.weight,
            slant=self.style,
        )
        self.display_list.append((self.cursor_x, self.cursor_y, word, wordFont))
        self.cursor_x += w + self.font.measure(" ")
        if self.cursor_x + w > self.width - hstep:
            self.cursor_x = hstep
            self.cursor_y += self.font.metrics("linespace") * 1.25
