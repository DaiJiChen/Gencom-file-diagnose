import unittest
import Parser
import validate

class TestUS13(unittest.TestCase):
    # A successful case
    def test_US13(self):
        gc = Parser.Gedcom(["gedcomfile.ged"])
        self.assertEqual(validate.siblingSpace(gc), 1)
    # A failure case
    def test_US13(self):
        gc = Parser.Gedcom(["bad_gedcomfile.ged"])
        self.assertEqual(validate.siblingSpace(gc), 0)


unittest.main()