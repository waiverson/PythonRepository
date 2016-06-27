# coding=utf-8
__author__ = 'xyc'


import copy,sys



"""
The Prototype Pattern is used to create new objects by cloning an original object,
and then modifying the clone.
"""

class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_object(Class, *args, **kwargs):
    return Class(*args, **kwargs)

#Given this classic Point class, here are seven ways to create new points:
point1 = Point(1, 2)
point2 = eval("{}({}, {})".format("Point", 2, 4)) # Risky
point3 = getattr(sys.modules[__name__], "Point")(3, 6)
point4 = globals()["Point"](4, 8)
point5 = make_object(Point, 5, 10)
point6 = copy.deepcopy(point5)
point6.x = 6
point6.y = 12
point7 = point1.__class__(7, 14) # Could have used any of point1 to point6