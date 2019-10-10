import unittest
import Parser
import validate

class TestUS04(unittest.TestCase):
    # A successful case
    def test_US04(self):
        gc = Parser.Gedcom(["gedcomfile.ged"])
        self.assertEqual(validate.divBeforeMarr(gc), 1)
    # A failure case
    def test_US04(self):
        gc = Parser.Gedcom(["bad_gedcomfile.ged"])
        self.assertEqual(validate.divBeforeMarr(gc), 0)


unittest.main()
