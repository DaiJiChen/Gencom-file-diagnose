import unittest
import Parser
import validate

class TestUS22(unittest.TestCase):
    # A successful case
    def test_US22(self):
        gc = Parser.Gedcom(["gedcomfile.ged"])
        self.assertEqual(validate.duplicateID(gc), 1)
    # A failure case
    def test_US22(self):
        gc = Parser.Gedcom(["bad_gedcomfile.ged"])
        self.assertEqual(validate.duplicateID(gc), 0)


unittest.main()
