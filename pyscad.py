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
        stream.write("cube(size = [%f, %f, %f], center = %s);\n" % (
            self.w, self.d, self.h, self.center))


class Union(object):
    """ Creates a union of one or more objects."""
    
    def __init__(self, *objects):
        self.objects = objects

    def render(self, stream, indent=0):
        stream.write(indentate(indent))
        stream.write("union() {\n")
        for o in self.objects:
            o.render(stream, indent + 2)
        stream.write(indentate(indent))
        stream.write("}\n")

        
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
        stream.write("sphere(r = %f);\n" % self.radius)


class Cylinder(object):
    """Creates a cylinder.

    This is an object with equal top and bottom radius the exact equivalent
    of OpenSCAD's 'cylinder' is TruncatedCone.

    Cylinder(radius=nnn, height=nnn)
      or
    Cylinder(diameter=nnn, height=nnn)
    """

    def __init__(self, radius=None, diameter=None, height=None, center=False):
        if not height:
            raise ParameterError(
                "Cylinder expects to be passed heght, none detected.")
        if radius or diameter:
            if radius and diameter:
                raise ParameterError(
                    "Cylinder expects exactly one of radius"
                    " or diameter, passed radius = %s, diameter = %s",
                    radius, diameter)
            if radius:
                self.diameter = radius * 2.0
            else:
                self.diameter = diameter
            self.height = height
            self.center = center
        else:
            raise ParameterError(
                "Cylinder expects radius or diameter, neither passed.")

    def render(self, stream, indent=0):
        center = "false"
        if self.center:
            center = "true"
        stream.write(indentate(indent))
        stream.write("cylinder(h = %f, d = %f, center = %s);\n" %
                     (self.height, self.diameter, center))


class TruncatedCone(object):
    """The TruncatedCone takes a bottom radius/diameter (r1/d1), a top
    radius/diameeter (r2/d2) and a height (height). It generated an
    OpenSCAD cylinder."""

    def __init__(self, r1=None, r2 = None, d1=None, d2=None, height=None, center=False):
        if (r1 and d1) or (r2 and d2):
            raise ParameterError(
                "TruncatedCone, cannot specify both radius and diameter.")
        if not (r1 or d1):
            raise ParameterError("TruncatedCone, no bottom radius or diameter")
        if not (r2 or d2):
            raise ParameterError("TruncatedCone, no top radius or diameter")
        if not height:
            raise ParameterError("TruncatedCone, no height")
            
        if r1:
            self.d1 = r1 * 2.0
        else:
            self.d1 = d1
        if r2:
            self.d2 = r2 * 2.0
        else:
            self.d2 = d2
        self.height = height
        self.center = center

    def render(self, stream, indent=0):
        center = "false"
        if self.center:
            center = "true"
        stream.write(indentate(indent))
        stream.write("cylinder(h = %f, d1 = %f, d2 = %f, center = %s);\n" %
                     (self.height, self.d1, self.d2, center))


class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "[%f, %f, %f]" % (self.x, self.y, self.z)

