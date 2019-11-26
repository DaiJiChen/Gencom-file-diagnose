import unittest
import Parser
import validate

class TestUS16(unittest.TestCase):
    # A successful case
    def pass_US23(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        self.assertEqual(validate.uniqueNameBirth(gc), 1)
    # A failure case
    def fail_US23(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        self.assertEqual(validate.uniqueNameBirth(gc), 0)


unittest.main()
