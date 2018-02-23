import unittest
import StringIO

import pyscad


class BoxTest(unittest.TestCase):
    def testNoParameters(self):
        self.assertRaises(pyscad.ParameterError, pyscad.Box)

    def testAllParameters(self):
        self.assertRaises(pyscad.ParameterError,
                          pyscad.Box, side=1, width=2, height=3, depth=4)

    def testNoWidth(self):
        self.assertRaises(pyscad.ParameterError,
                          pyscad.Box, height=3, depth=4)
    def testNoDepth(self):
        self.assertRaises(pyscad.ParameterError,
                          pyscad.Box, width=2, height=3)
    def testNoHeight(self):
        self.assertRaises(pyscad.ParameterError,
                          pyscad.Box, width=2, depth=4)
    def testSideAndOne(self):
        self.assertRaises(pyscad.ParameterError,
                          pyscad.Box, side=1, width=2)

    def testSideOnly(self):
        b = pyscad.Box(side=1.0)
        self.assertEqual(1.0, b.w)
        self.assertEqual(1.0, b.d)
        self.assertEqual(1.0, b.h)

    def testExplicit(self):
        b = pyscad.Box(width=1.0, depth=4.0, height=9.0)
        self.assertEqual(1.0, b.w)
        self.assertEqual(4.0, b.d)
        self.assertEqual(9.0, b.h)

    def testRender1(self):
        dump = StringIO.StringIO()
        b = pyscad.Box(width=1.0, depth=4.0, height=9.0)
        b.render(dump)
        seen = dump.getvalue()
        expected = 'cube(size = [1.000000, 4.000000, 9.000000], center = false);\n'
        self.assertEqual(seen, expected)


class SphereTest(unittest.TestCase):
    def testNoParameters(self):
        self.assertRaises(pyscad.ParameterError, pyscad.Sphere)

    def testAllParameters(self):
        self.assertRaises(pyscad.ParameterError, pyscad.Sphere,
                          radius=1.0, diameter=2.0)

    def testPassRadius(self):
        s = pyscad.Sphere(radius=1.0)
        self.assertEqual(s.radius, 1.0)

    def testPassDiameter(self):
        s = pyscad.Sphere(diameter=2.0)
        self.assertEqual(s.radius, 1.0)

    def testRender(self):
        dump = StringIO.StringIO()
        s = pyscad.Sphere(radius=1.0)
        s.render(dump)
        seen = dump.getvalue()
        expected = 'sphere(r = 1.000000);\n'
        self.assertEqual(seen, expected)


class UnionTest(unittest.TestCase):

    def testUnionNoObjects(self):
        dump = StringIO.StringIO()
        u = pyscad.Union()
        u.render(dump)
        expected = 'union() {\n}\n'
        seen = dump.getvalue()
        self.assertEqual(seen, expected)

    def testSingleObject(self):
        dump = StringIO.StringIO()
        u = pyscad.Union(pyscad.Sphere(radius=1.0))
        u.render(dump)
        expected = 'union() {\n  sphere(r = 1.000000);\n}\n'
        seen = dump.getvalue()
        self.assertEqual(seen, expected)
        
    def testMultipleObjects(self):
        dump = StringIO.StringIO()
        u = pyscad.Union(pyscad.Sphere(radius=1.0), pyscad.Sphere(radius=2.0))
        u.render(dump)
        expected = 'union() {\n  sphere(r = 1.000000);\n  sphere(r = 2.000000);\n}\n'
        seen = dump.getvalue()
        self.assertEqual(seen, expected)

                
if __name__ == '__main__':
    unittest.main()
