import unittest
import Parser
import validate

class TestUS02(unittest.TestCase):
    # A successful case
    def test_US02(self):
        gc = Parser.Gedcom(["gedcomfile.ged"])
        self.assertEqual(validate.multiBirthLessThan5(gc), 1)
    # A failure case
    def test_US02(self):
        gc = Parser.Gedcom(["bad_gedcomfile.ged"])
        self.assertEqual(validate.multiBirthLessThan5(gc), 0)


if __name__ == '__main__':
    unittest.main()