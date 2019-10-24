import unittest
import Parser
import validate

class TestUS12(unittest.TestCase):
    # A successful case
    def test_US12(self):
        gc = Parser.Gedcom(["gedcomfile.ged"])
        self.assertEqual(validate.parrTooOld(gc), 1)
    # A failure case
    def test_US12(self):
        gc = Parser.Gedcom(["bad_gedcomfile.ged"])
        self.assertEqual(validate.parrTooOld(gc), 0)


unittest.main()