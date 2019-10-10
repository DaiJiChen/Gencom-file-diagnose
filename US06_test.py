"""
@author: zzhan
"""

import unittest
import Parser
import validate

class Testing(unittest.TestCase):

    def test1(self):
        gc = Parser.Gedcom("US06a.ged")
        self.assertEqual(validate.DivorceBeforeDeath(gc),1)

        
    def test2(self):
        gc = Parser.Gedcom("US06b.ged")
        self.assertEqual(validate.DivorceBeforeDeath(gc),0)
    

        

unittest.main()
