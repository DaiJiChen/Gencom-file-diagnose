import unittest
import Parser
import validate

class TestUS07(unittest.TestCase):
    # A successful case
    def test_US10(self):
        gc = Parser.Gedcom(["US10a.ged"])
        self.assertEqual(validate.marrAfter14(gc), 1)
    # A failure case
    def test_US10(self):
        gc = Parser.Gedcom(["US10b.ged"])
        self.assertEqual(validate.marrAfter14(gc), 1)


unittest.main()