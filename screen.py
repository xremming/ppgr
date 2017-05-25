import shutil
import sys


class Screen:
    _braille_base = 0x2800
    _braille_dot = (
        (0x01, 0x08),
        (0x02, 0x10),
        (0x04, 0x20),
        (0x40, 0x80))
    braille_width = 2
    braille_height = 4

    @staticmethod
    def _braille_subpixel(x, y):
        return Screen._braille_dot[y][x]

    def __init__(self, width=None, height=None, to_int=int):
        self._width = 0
        self._height = 0

        self.width = width
        self.height = height

        self._round = to_int

        self.clear()

    @property
    def width(self):
        return self._width * Screen.braille_width

    @width.setter
    def width(self, width):
        if width is None:
            width, _ = shutil.get_terminal_size()
            width *= Screen.braille_width
        width -= width % Screen.braille_width

        self._width = width // Screen.braille_width
        self.clear()

    @property
    def height(self):
        return self._height * Screen.braille_height

    @height.setter
    def height(self, height):
        if height is None:
            _, height = shutil.get_terminal_size()
            height *= Screen.braille_height
        height -= height % Screen.braille_height

        self._height = height // Screen.braille_height
        self.clear()

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, width_height):
        try:
            self.width, self.height = width_height
        except TypeError as e:
            raise TypeError("Setting size requires an iterable with two values ({}).".format(e))

    def clear(self):
        self._screen = [[Screen._braille_base for _ in range(self._width)] for _ in range(self._height)]

    def __call__(self, x, y, mode=True):
        px, py = x // Screen.braille_width, y // Screen.braille_height
        px, py = self._round(px), self._round(py)
        sp = Screen._braille_subpixel(
            self._round(x % Screen.braille_width),
            self._round(y % Screen.braille_height))

        if mode is True:
            # turn x, y on
            self._screen[py][px] |= sp
        elif mode is False:
            # turn x, y off
            self._screen[py][px] |= ~sp
        elif mode is None:
            # toggle x, y
            self._screen[py][px] ^= sp
        else:
            raise TypeError("Mode must be one of (True, False, None).")

    def __str__(self):
        out = []
        for line in self._screen:
            out.append("".join(map(chr, line)))
        return "\n".join(out)
