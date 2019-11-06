import unittest
import Parser
import validate

class TestUS07(unittest.TestCase):
    # A successful case
    def test_US07(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        self.assertEqual(validate.under150(gc), 1)
    # A failure case
    def test_US07(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        self.assertEqual(validate.under150(gc), 0)


unittest.main()
