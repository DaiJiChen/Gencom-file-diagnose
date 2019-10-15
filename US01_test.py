import unittest
import Parser
import validate

class TestUS02(unittest.TestCase):
    # A successful case
    def test_US02(self):
        gc = Parser.Gedcom(["gedcomfile.ged"])
        self.assertEqual(validate.birtDeatB4CurrDate(gc), 1)
        self.assertEqual(validate.marrDivB4CurrDate(gc), 1)

    # A failure case
    def test_US02(self):
        gc = Parser.Gedcom(["bad_gedcomfile.ged"])
        self.assertEqual(validate.birtDeatB4CurrDate(gc), 0)
        self.assertEqual(validate.marrDivB4CurrDate(gc), 0)


if __name__ == '__main__':
    unittest.main()