from abc import ABC, abstractmethod
import math

END = '\033[0'
START = '\033[1;38;2'
MOD = 'm'


class ComputerColor(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __rmul__(self, other):
        pass


class RGBColor(ComputerColor):
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f'{START};{self.red};{self.green};{self.blue}{MOD}●{END}{MOD}'

    def __eq__(self, other):
        return (
            self.red == other.red
            and self.green == other.green
            and self.blue == other.blue
        )

    def __add__(self, other):
        red = self.red + other.red
        green = self.green + other.green
        blue = self.blue + other.blue
        return RGBColor(red, green, blue)

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __repr__(self):
        return f'{START};{self.red};{self.green};{self.blue}{MOD}●{END}{MOD}'

    def __mul__(self, other):
        cl = -1 * 256 * (1 - other)
        f = (259 * (cl + 255)) / (255 * (259 - cl))
        return RGBColor(
            int(f * (self.red - 128) + 128),
            int(f * (self.green - 128) + 128),
            int(f * (self.blue - 128) + 128),
        )

    __rmul__ = __mul__


class HSLColor(ComputerColor):
    def __init__(self, hue: int, saturation: int, lightness: int):
        self.hue = hue
        self.saturation = saturation
        self.lightness = lightness

    def __repr__(self):
        r, g, b = hsl_to_rgb_convertor(HSLColor(self.hue, self.saturation, self.lightness))
        return f'{START};{r};{g};{b}{MOD}●{END}{MOD}'

    def __mul__(self, other):
        """
        Функция для умножения. Возвращает RGBColor объект. 
        """
        r, g, b = hsl_to_rgb_convertor(HSLColor(self.hue, self.saturation, self.lightness))
        cl = -1 * 256 * (1 - other)
        f = (259 * (cl + 255)) / (255 * (259 - cl))
        return RGBColor(
            int(f * (r - 128) + 128),
            int(f * (g - 128) + 128),
            int(f * (b - 128) + 128),
        )

    __rmul__ = __mul__


def print_a(color: ComputerColor):
    bg_color = 0.2 * color
    a_matrix = [
        [bg_color] * 19,
        [bg_color] * 9 + [color] + [bg_color] * 9,
        [bg_color] * 8 + [color] * 3 + [bg_color] * 8,
        [bg_color] * 7 + [color] * 2 + [bg_color] + [color] * 2 + [bg_color] * 7,
        [bg_color] * 6 + [color] * 2 + [bg_color] * 3 + [color] * 2 + [bg_color] * 6,
        [bg_color] * 5 + [color] * 9 + [bg_color] * 5,
        [bg_color] * 4 + [color] * 2 + [bg_color] * 7 + [color] * 2 + [bg_color] * 4,
        [bg_color] * 3 + [color] * 2 + [bg_color] * 9 + [color] * 2 + [bg_color] * 3,
        [bg_color] * 19,
    ]
    for row in a_matrix:
        print(''.join(str(ptr) for ptr in row))


def hsl_to_rgb_convertor(HSL: HSLColor):
    """
    Принимает на вход HSL объект
    Возвращает его в формате r, g, b компонентах
    """
    h = HSL.hue
    s = HSL.saturation / 100
    l = HSL.lightness / 100
    c = (1 - math.fabs(2 * l - 1)) * s
    x = c * (1 - math.fabs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r1 = c
        g1 = x
        b1 = 0
    elif 60 <= h < 120:
        r1 = x
        g1 = c
        b1 = 0
    elif 120 <= h < 180:
        r1 = 0
        g1 = c
        b1 = x
    elif 180 <= h < 240:
        r1 = 0
        g1 = x
        b1 = c
    elif 240 <= h < 300:
        r1 = x
        g1 = 0
        b1 = c
    elif 300 <= h < 360:
        r1 = c
        g1 = 0
        b1 = x
    r = (r1 + m) * 255
    g = (g1 + m) * 255
    b = (b1 + m) * 255
    return int(r), int(g), int(b)


if __name__ == '__main__':
    red = RGBColor(255, 0, 0)
    print(red)
    print_a(red)

    red_hsl = HSLColor(300, 100, 50)
    print(hsl_to_rgb_convertor(red_hsl))
    print(red_hsl)
    print_a(red_hsl)
