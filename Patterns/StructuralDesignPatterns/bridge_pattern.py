__author__ = 'xyc'

# The Bridge Pattern is used in situations where we want to separate an abstraction
# (e.g., an interface or an algorithm) from how it is implemented.

import abc

"""
has_methods() function captures the required methods
and creates a class decorator function, which it then returns. The decorator itself
creates a __subclasshook__() function, and then adds it to the base class
as a class method using the built-in classmethod() function.
"""
def has_methods(*methods):
    def decorator(Base):
        def __subclasshook__(Class, Subclass):
            if Class is Base:
                attributes = collections.ChainMap(*(Superclass.__dict__ for Superclass in Subclass.__mro__))
                if all(method in attributes for method in methods):
                    return True
            return NotImplemented
        Base.__subclasshook__ = classmethod(__subclasshook__)
        return Base
    return decorator

@has_methods("initialize", "draw_caption", "draw_bar", "finalize")
class BarRenderer(metaclass=abc.ABCMeta): pass

class BarCharter:
    def __init__(self, renderer):
        if not isinstance(renderer, BarRenderer):
            raise TypeError("Expected object of type BarRenderer, got {}".format(type(renderer).__name__))
        self.__renderer = renderer

    def render(self, caption, pairs):
        maximum = max(value for _, value in pairs)
        self.__renderer.initialize(len(pairs), maximum)
        self.__renderer.draw_caption(caption)
        for name, value in pairs:
            self.__renderer.draw_bar(name, value)
        self.__renderer.finalize()


class TextBarRenderer:
    def __init__(self, scaleFactor=40):
        self.scaleFactor = scaleFactor

    def initialize(self, bars, maximum):
        assert bars > 0 and maximum > 0
        self.scale = self.scaleFactor / maximum

    def draw_caption(self, caption):
        print("{0:^{2}}\n{1:^{2}}".format(caption, "=" * len(caption), self.scaleFactor))

    def draw_bar(self, name, value):
        print("{} {}".format("*" * int(value * self.scale), name))

    def finalize(self):
        pass

class ImageBarRenderer:
    COLORS = [Image.color_for_name(name) for name in ("red", "green",
                                        "blue", "yellow", "magenta", "cyan")]

    def __init__(self, stepHeight=10, barWidth=30, barGap=2):
        self.stepHeight = stepHeight
        self.barWidth = barWidth
        self.barGap = barGap

    def initialize(self, bars, maximum):
        assert bars > 0 and maximum > 0
        self.index = 0
        color = Image.color_for_name("white")
        self.image = Image.Image(bars * (self.barWidth + self.barGap),
                                maximum * self.stepHeight, background=color)

    def draw_caption(self, caption):
        self.filename = os.path.join(tempfile.gettempdir(), re.sub(r"\W+", "_", caption) + ".xpm")

    def draw_bar(self, name, value):
        color = ImageBarRenderer.COLORS[self.index % len(ImageBarRenderer.COLORS)]
        width, height = self.image.size
        x0 = self.index * (self.barWidth + self.barGap)
        x1 = x0 + self.barWidth
        y0 = height - (value * self.stepHeight)
        y1 = height - 1
        self.image.rectangle(x0, y0, x1, y1, fill=color)
        self.index += 1

    def finalize(self):
        self.image.save(self.filename)
        print("wrote", self.filename)

def main():
    pairs = (("Mon", 16), ("Tue", 17), ("Wed", 19), ("Thu", 22), ("Fri", 24), ("Sat", 21), ("Sun", 19))
    textBarCharter = BarCharter(TextBarRenderer())
    textBarCharter.render("Forecast 6/8", pairs)
    imageBarCharter = BarCharter(ImageBarRenderer())
    imageBarCharter.render("Forecast 6/8", pairs)