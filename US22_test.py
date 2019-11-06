import unittest
import Parser
import validate


class Testing(unittest.TestCase):
    # A successful case
    def test1(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        self.assertEqual(len(gc.duplicateIndi) + len(gc.duplicateFam), 0)

    # A failure case
    def test2(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        self.assertNotEqual(len(gc.duplicateIndi) + len(gc.duplicateFam), 0)


unittest.main()