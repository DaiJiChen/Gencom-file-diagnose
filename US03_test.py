import unittest
import Parser
import validate

class TestUS03(unittest.TestCase):
    # A successful case
    def test_US03(self):
        gc = Parser.Gedcom(["US03a.ged"])
        self.assertEqual(validate.BirtBeforeDeat(gc), 1)
    # A failure case
    def test_US03(self):
        gc = Parser.Gedcom(["US03b.ged"])
        self.assertEqual(validate.BirtBeforeDeat(gc), 0)


if __name__ == '__main__':
    unittest.main()