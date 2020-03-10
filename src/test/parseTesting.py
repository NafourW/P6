import unittest


class ParseTesting(unittest.TestCase):
    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_01(self):
        self.assertEqual(10, 10)


if __name__ == "__main__":
    unittest.main()
