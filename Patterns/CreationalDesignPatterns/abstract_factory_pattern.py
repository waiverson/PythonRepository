# encoding: 'utf-8'
__author__ = 'xyc'


"""此case只是该模式用法的结构，非可执行代码"""

"""sample one"""
def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    text = factory.make_text(7, 3, "Abstract Factory")
    diagram.add(rectangle)
    diagram.add(text)
    return  diagram

def main():
    # ...
    txtDiagram = create_diagram(DiagramFactory())
    txtDiagram.save(textFilename)
    svgDiagram = create_diagram(SvgDiagramFactory())
    svgDiagram.save(svgFilename)

class DiagramFactory:
    def make_diagram(self, width, height):
        return Diagram(width, height)

    def make_rectangle(self, x, y, width, height, fill="white", stroke="black"):
        return Rectangle(x, y, width, height, fill, stroke)

    def make_text(self, x, y, text, fontsize=12):
        return Text(x, y, text, fontsize)

class SvgDiagramFactory(DiagramFactory):
    def make_diagram(self, width, height):
        return SvgDiagram(width, height)

    def make_text(*args):
        return SvgText()
    # ...

class Diagram():
    # ...
    def add(self, component):
        for y, row in enumerate(component.rows):
            for x, char in enumerate(row):
                self.diagram[y + component.y][x + component.x] = char

class Rectangle():
    pass

class Text():
    def __init__(self, x, y, text, fontsize):
        self.x = x
        self.y = y
        self.rows = [list(text)]

class SvgDiagram():
    # ...
    def add(self, component):
        self.diagram.append(component.svg)

class SvgRectangle():
    pass

SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" \
font-family="sans-serif" font-size="{fontsize}">{text}</text>"""
SVG_SCALE = 20
class SvgText:
    def __init__(self, x, y, text, fontsize):
        x *= SVG_SCALE
        y *= SVG_SCALE
        fontsize *= SVG_SCALE // 10
        self.svg = SVG_TEXT.format(**locals())


"""sample two ,more pythonic"""

def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    text = factory.make_text(7, 3, "Abstract Factory")
    diagram.add(rectangle)
    diagram.add(text)
    return diagram

def main():

    txtDiagram = create_diagram(DiagramFactory)
    txtDiagram.save(textFilename)
    svgDiagram = create_diagram(SvgDiagramFactory)
    svgDiagram.save(svgFilename)

class DiagramFactory:

    class Diagram:
        pass

    class Rectangle:
        pass

    class Text:
        pass

    @classmethod
    def make_diagram(cls, width, height):
        return cls.Diagram(width, height)

    @classmethod
    def make_rectangle(cls, x, y, width, height, fill="white", stroke="black"):
        return cls.Rectangle(x, y, width, height, fill, stroke)

    @classmethod
    def make_text(cls, x, y, text, fontsize=12):
        return cls.Text(x, y, text, fontsize)


class SvgDiagramFactory(DiagramFactory):

    SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" \
                    font-family="sans-serif" font-size="{fontsize}">{text}</text>"""
    SVG_SCALE = 20

    class Text:
        def __init__(self, x, y, text, fontsize):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            fontsize *= SvgDiagramFactory.SVG_SCALE // 10
            self.svg = SvgDiagramFactory.SVG_TEXT.format(**locals())

    class Diagram:
        pass

    class Rectangle:
        pass
