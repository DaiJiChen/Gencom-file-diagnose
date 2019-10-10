import unittest
import Parser
import validate

class TestUS02(unittest.TestCase):
    # A successful case
    def test_US02(self):
        gc = Parser.Gedcom(["US02a.ged"])
        self.assertEqual(validate.BirtBeforeMarr(gc), 1)
    # A failure case
    def test_US02(self):
        gc = Parser.Gedcom(["US02b.ged"])
        self.assertEqual(validate.BirtBeforeMarr(gc), 1)


if __name__ == '__main__':
    unittest.main()