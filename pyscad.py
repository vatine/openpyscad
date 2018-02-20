#! /usr/bin/env python

"""A small hack to allow generation of OpenSCAD models using a more
Pythonic interace."""


class ParameterError(Exception):
    def __init__(self, fmt, *args):
        self.data = fmt % args

    def __str__(self):
        return self.data

    
def indentate(n):
    return ''.join([' '] * n)


class Box(object):
    """Create a box.

    You will need to specify eiter side or all of width, depth,
    and height."""
    def __init__(self, side=0, width=0, height=0, depth=0, center=False):
        if side:
            if width or height or depth:
                raise ParameterError("Unexpected side, as well as"
                                     " w/d/h parameters specified.")
            self.w = side
            self.h = side
            self.d = side
        elif width and height and depth:
            self.w = width
            self.h = height
            self.d = depth
        else:
            raise ParameterError("Box requires one of 'side' or 'width, depth, height'.")
        self.center="true" if center else "false"

    def render(self, stream, indent=0):
        stream.write(indentate(indent))
        stream.write("cube(size = [%f, %f, %f], center = %s)\n" % (
            self.w, self.d, self.h, self.center))


class Union(object):
    """ Creates a union of one or more objects."""
    
    def __init__(self, *objects):
        self.objects = objects

    def render(self, stream, indent=0):
        self.write(indentate(indent))
        self.write("union() {\n")
        for o in self.objects:
            o.render(stream, indent + 2)
        self.write(indentate(indent))
        self.write("}\n")

        
class Translate(object):
    """Translates one or more objects.

    Takes delta x, y, and z, as well as the object(s) to translate."""
    
    def __init__(self, dx, dy, dz, *objects):
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.objects = objects

    def render(self, stream, indent=0):
        self.write(indentate(indent))
        self.write("translate (v =[%f, %f, %f]) {\n" % (self.dx, self.dy,
                                                        self.dz))
        for o in self.objects:
            o.render(stream, indent + 2)
        self.write(indentate(indent))
        self.write("}\n")


class Sphere(object):
    """Creates a sphere.

    You will need to specify exactly one of radius or diameter."""

    def __init__(self, radius=None, diameter=None):
        nones = 0
        if radius is None:
            nones += 1
        if diameter is None:
            nones += 1
        if nones != 1:
            raise ParameterError("Sphere expects exactly one of radius and diameters, passed radius = %s, diameter = %s", radius, diameter)

        if radius:
            self.radius = radius
        if diameter:
            self.radius = diameter / 2.0

    def render(self, stream, indent=0):
        stream.write(indentate(indent))
        stream.write("sphere(r = %f)\n" % self.radius)
