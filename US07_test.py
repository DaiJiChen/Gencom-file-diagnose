import unittest
import Parser
import validate

class TestUS07(unittest.TestCase):
    # A successful case
    def test_US02(self):
        gc = Parser.Gedcom(["US07a.ged"])
        self.assertEqual(validate.under150(gc), 1)
    # A failure case
    def test_US02(self):
        gc = Parser.Gedcom(["US07b.ged"])
        self.assertEqual(validate.under150(gc), 1)


unittest.main()