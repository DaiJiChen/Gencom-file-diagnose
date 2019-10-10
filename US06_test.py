"""
@author: zzhan
"""

import unittest
import Parser
import validate

class Testing(unittest.TestCase):
    # A successful case
    def test1(self):
        gc = Parser.Gedcom("US06a.ged")
        self.assertEqual(validate.DivorceBeforeDeath(gc),1)

    # A failure case    
    def test2(self):
        gc = Parser.Gedcom("US06b.ged")
        self.assertEqual(validate.DivorceBeforeDeath(gc),0)
    

        
unittest.main()
