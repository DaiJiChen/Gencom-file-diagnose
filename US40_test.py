import unittest
import Parser
import validate


class Testing(unittest.TestCase):
    # A successful case
    def test1(self):
        self.assertEqual(Parser.main("gedcomfile.ged", []), 0)

    # A failure case
    def test2(self):
        self.assertEqual(Parser.main("gedcomfile.ged", []), 0)


unittest.main()