# encoding: 'utf-8'
__author__ = 'xyc'


"""
The Adapter Pattern is a technique for adapting an interface so that one class
can make use of another class—that has an incompatible interface—without
changing either of the classes being used.
"""

import abc,collections,sys,textwrap
from re import escape

class Page: # 这个类充当了适配器功能
    def __init__(self, title, renderer):
        if not isinstance(renderer, Renderer):
            raise TypeError("Expected object of type Renderer, got {}".format(type(renderer).__name__))
        self.title = title
        self.renderer = renderer
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def render(self):
        self.renderer.header(self.title)
        for paragraph in self.paragraphs:
            self.renderer.paragraph(paragraph)
        self.renderer.footer()

class Renderer(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, Subclass):
        if cls is Renderer:
            attributes = collections.ChainMap(*(Superclass.__dict__
                for Superclass in Subclass.__mro__))
            methods = ("header", "paragraph", "footer")
            if all(method in attributes for method in methods):
                return True
        return NotImplemented

class TextRenderer:
    def __init__(self, width=80, file=sys.stdout):
        self.width = width
        self.file = file
        self.previous = False

    def header(self, title):
        self.file.write("{0:^{2}}\n{1:^{2}}\n".format(title,
        "=" * len(title), self.width))

    def paragraph(self, text):
        if self.previous:
            self.file.write("\n")
        self.file.write(textwrap.fill(text, self.width))
        self.file.write("\n")
        self.previous = True

    def footer(self):
        pass


class HtmlWriter:
    def __init__(self, file=sys.stdout):
        self.file = file

    def header(self):
        self.file.write("<!doctype html>\n<html>\n")

    def title(self, title):
        self.file.write("<head><title>{}</title></head>\n".format(escape(title)))

    def start_body(self):
        self.file.write("<body>\n")

    def body(self, text):
        self.file.write("<p>{}</p>\n".format(escape(text)))

    def end_body(self):
        self.file.write("</body>\n")

    def footer(self):
        self.file.write("</html>\n")

class HtmlRenderer:
    def __init__(self, htmlWriter):
        self.htmlWriter = htmlWriter

    def header(self, title):
        self.htmlWriter.header()
        self.htmlWriter.title(title)
        self.htmlWriter.start_body()

    def paragraph(self, text):
        self.htmlWriter.body(text)

    def footer(self):
        self.htmlWriter.end_body()
        self.htmlWriter.footer()

textPage = Page(title, TextRenderer(22))
textPage.add_paragraph(paragraph1)
textPage.add_paragraph(paragraph2)
textPage.render()
htmlPage = Page(title, HtmlRenderer(HtmlWriter(file)))
htmlPage.add_paragraph(paragraph1)
htmlPage.add_paragraph(paragraph2)
htmlPage.render()