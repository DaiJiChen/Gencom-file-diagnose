"""
@author: zzhan
"""

import unittest
import Parser
import validate

class Testing(unittest.TestCase):
    # A successful case
    def test1(self):
        gc = Parser.Gedcom("gedcomfile.ged")
        self.assertEqual(validate.MarriageBeforeDeath(gc),1)
    # A failure case    
    def test2(self):
        gc = Parser.Gedcom("bad_gedcomfile.ged")
        self.assertEqual(validate.MarriageBeforeDeath(gc),0)

        

    

        
unittest.main()
