import unittest
import Parser
import validate


class Testing(unittest.TestCase):
    # A successful case
    def test1(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        emptyAge = 0
        for indiID, indi in gc.individuals.items():
            if indi.age == None:
                emptyAge = 1
        self.assertEqual(emptyAge, 0)

    # A failure case
    def test2(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        emptyAge = 0
        for indiID, indi in gc.individuals.items():
            if indi.age == None:
                emptyAge = 1
        self.assertEqual(emptyAge, 0)


unittest.main()