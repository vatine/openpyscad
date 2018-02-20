import unittest
import StringIO

import pyscad

class SphereTest(unittest.TestCase):

    def testNoParameters(self):
        self.assertRaises(pyscad.ParameterError, pyscad.Sphere)

    def testTwoParameters(self):
        self.assertRaises(pyscad.ParameterError, pyscad.Sphere, 1, 1)

    def testSpecifyRadius(self):
        s = pyscad.Sphere(radius=1.0)
        self.assertEqual(1.0, s.radius)

    def testSpecifyDiameter(self):
        s = pyscad.Sphere(diameter=2.0)
        self.assertEqual(1.0, s.radius)

    def testRender(self):
        dump = StringIO.StringIO()
        s = pyscad.Sphere(diameter=2.0)
        s.render(dump)
        seen = dump.getvalue()
        expected = 'sphere(r = 1.000000)\n'
        self.assertEqual(seen, expected)

        
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
        expected = 'cube(size = [1.000000, 4.000000, 9.000000], center = false)\n'
        self.assertEqual(seen, expected)


if __name__ == '__main__':
    unittest.main()
