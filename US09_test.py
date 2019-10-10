import unittest
import Parser
import validate

class TestUS09(unittest.TestCase):
    # A successful case
    def test_US09(self):
        gc = Parser.Gedcom(["US09a.ged"])
        self.assertEqual(validate.duplicateID(gc), 1)
    # A failure case
    def test_US09(self):
        gc = Parser.Gedcom(["US09b.ged"])
        self.assertEqual(validate.duplicateID(gc), 1)


unittest.main()