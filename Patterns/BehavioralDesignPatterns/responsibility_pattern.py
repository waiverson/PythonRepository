__author__ = 'xyc'

import functools

# The Chain of Responsibility Pattern is designed to decouple the sender of a
# request from the recipient that processes the request.


def coroutine(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator
    return wrapper


@coroutine
def key_handler(successor=None):
    while True:
        event = (yield)
        if event.kind == Event.KEYPRESS:
            print("Press: {}".format(event))
        elif successor is not None:
            successor.send(event)
@coroutine
def mouse_handler(successor=None):
    while True:
        event = (yield)
        if event.kind == Event.Mouse:
            print("Click: {}".format(event))
        elif successor is not None:
            successor.send(event)

@coroutine
def debug_handler(successor, file=sys.stdout):
    while True:
        event = (yield)
        file.write("*DEBUG*: {}\n".format(event))
        successor.send(event)

# In this example, the value will first be
# sent to the key_handler() coroutine, which will either handle the event or pass it on.
pipeline = key_handler(mouse_handler())
pipeline = debug_handler(pipeline)


while True:
    event = Event.next()
    if event.kind == Event.TERMINATE:
        break
    pipeline.send(event)