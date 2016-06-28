__author__ = 'xyc'

# The Mediator Pattern provides a means of creating an object—the mediator
# —that can encapsulate the interactions between other objects.

# sample one a conventional mediator
# mediator 作为中介，协调输入框text，按钮button与form直接的联动关系，text的改变通过mediator调用form的updateui
# button的状态改变，通过mediator调用form对象的clicked

import collections

class Mediator:
    def __init__(self, widgetCallablePairs):
        self.callablesForWidget = collections.defaultdict(list)
        for widget, caller in widgetCallablePairs:
            self.callablesForWidget[widget].append(caller)
            widget.mediator = self

    def on_change(self, widget):
        callables = self.callablesForWidget.get(widget)
        if callables is not None:
            for caller in callables:
                caller(widget)
        else:
            raise AttributeError("No on_change() method registered for {}".format(widget))

class Mediated:
    def __init__(self):
        self.mediator = None

    def on_change(self):
        if self.mediator is not None:
            self.mediator.on_change(self)

class Button(Mediated):
    def __init__(self, text=""):
        super().__init__()
        self.enabled = True
        self.text = text

    def click(self):
        if self.enabled:
            self.on_change()

class Text(Mediated):
    def __init__(self, text=""):
        super().__init__()
        self.__text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if self.text != text:
            self.__text = text
            self.on_change()

class Form:
    def __init__(self):
        self.create_widgets()
        self.create_mediator()

    def create_widgets(self):
        self.nameText = Text()
        self.emailText = Text()
        self.okButton = Button("OK")
        self.cancelButton = Button("Cancel")

    def create_mediator(self):
        self.mediator = Mediator(((self.nameText, self.update_ui),
                                    (self.emailText, self.update_ui),
                                    (self.okButton, self.clicked),
                                    (self.cancelButton, self.clicked)))
        self.update_ui()

    def update_ui(self, widget=None):
        self.okButton.enabled = (bool(self.nameText.text) and bool(self.emailText.text))

    def clicked(self, widget):
        if widget == self.okButton:
            print("OK")
        elif widget == self.cancelButton:
            print("Cancel")

# sample two a coroutine-based mediator

@coroutine
def _update_ui_mediator(self, successor=None):
    while True:
        widget = (yield)
    self.okButton.enabled = (bool(self.nameText.text) and bool(self.emailText.text))
    if successor is not None:
        successor.send(widget)

def create_mediator(self):
    self.mediator = self._update_ui_mediator(self._clicked_mediator())
    for widget in (self.nameText, self.emailText, self.okButton,self.cancelButton):
        widget.mediator = self.mediator
    self.mediator.send(None)

@coroutine
def _clicked_mediator(self, successor=None):
    while True:
        widget = (yield)
        if widget == self.okButton:
            print("OK")
        elif widget == self.cancelButton:
            print("Cancel")
        elif successor is not None:
            successor.send(widget)


class Mediated:
    def __init__(self):
        self.mediator = None

    def on_change(self):
        if self.mediator is not None:
            self.mediator.send(self)
