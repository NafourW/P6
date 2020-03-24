import unittest
from pyparsing import Word, nums, alphas, ParseException, alphanums


integer  = Word(nums)
var = Word(alphanums)
arithOp  = Word("+-*/", max=1)

expr = var + "=" + integer + arithOp + integer
equation = expr


class ParseTesting(unittest.TestCase):
    def test_01(self):
        test = "aa = 10 + 10"
        equation.parseString(test)

    def test_02(self):
        test = "a = 10 + a"
        with self.assertRaises(ParseException):
            equation.parseString(test)
    
    def test_03(self):
        test = "a = a + "
        with self.assertRaises(ParseException):
            equation.parseString(test)
    
    def test_04(self):
        test = "a = 1000 + 50"
        equation.parseString(test)


if __name__ == "__main__":
    unittest.main()
