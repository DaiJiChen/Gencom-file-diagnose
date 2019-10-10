"""
@author: zzhan
"""

import unittest
import Parser
import validate

class Testing(unittest.TestCase):

    def test1(self):
        gc = Parser.Gedcom("US05a.ged")
        self.assertEqual(validate.MarriageBeforeDeath(gc),1)
        
    def test2(self):
        gc = Parser.Gedcom("US05b.ged")
        self.assertEqual(validate.MarriageBeforeDeath(gc),0)    

        

    

        
unittest.main()
