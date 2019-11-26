import unittest
import Parser
import validate

class TestUS16(unittest.TestCase):
    # A successful case
    def test_US16(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        self.assertEqual(validate.maleLastNames(gc), 1)
    # A failure case
    def test_US16(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        self.assertEqual(validate.maleLastNames(gc), 0)


unittest.main()
