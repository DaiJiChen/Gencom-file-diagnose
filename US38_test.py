import unittest
import Parser
import validate

class Testing(unittest.TestCase):
    # A successful case
    def test_US38_1(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        self.assertEqual(gc.displayOutput("print US38"), 1)

    # A failure case
    def test_US38_2(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        self.assertEqual(gc.displayOutput("print US38"), 1)


if __name__ == '__main__':
    unittest.main()
