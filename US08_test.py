import unittest
import Parser
import validate

class TestUS08(unittest.TestCase):
    # A successful case
    def test_US08(self):
        gc = Parser.Gedcom(["US08a.ged"])
        self.assertEqual(validate.divBeforeMarr(gc), 1)
    # A failure case
    def test_US08(self):
        gc = Parser.Gedcom(["US08b.ged"])
        self.assertEqual(validate.divBeforeMarr(gc), 1)


unittest.main()