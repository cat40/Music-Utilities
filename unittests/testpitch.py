import unittest

import numpy
from audioutils import pitch


class MyTestCase(unittest.TestCase):
    def test_get_closest_value(self):
        array1 = numpy.asarray([1, 2, 3, 4, 5])
        array2 = numpy.asarray([0.5, 2, 900, 12, -1])
        array3 = numpy.asarray([0, 0, 0])
        array4 = numpy.asarray([])
        array5 = numpy.asarray([7])
        self.assertEqual(1, pitch.get_closest_value(array1, 0))
        self.assertEqual(2, pitch.get_closest_value(array1, 2))
        self.assertEqual(5, pitch.get_closest_value(array1, 10))
        self.assertEqual(2, pitch.get_closest_value(array1, 2.5))
        self.assertEqual(0.5, pitch.get_closest_value(array2, 1))
        self.assertEqual(12, pitch.get_closest_value(array2, 200))
        self.assertEqual(900, pitch.get_closest_value(array2, 1000))
        self.assertEqual(-1, pitch.get_closest_value(array2, -5))
        self.assertEqual(0, pitch.get_closest_value(array3, -1))
        self.assertEqual(0, pitch.get_closest_value(array3, 10))
        self.assertEqual(0, pitch.get_closest_value(array3, 0))
        self.assertRaises(ValueError, pitch.get_closest_value, array4, 1)
        self.assertEqual(7, pitch.get_closest_value(array5, 1))
        self.assertEqual(7, pitch.get_closest_value(array5, 7))


if __name__ == '__main__':
    unittest.main()
