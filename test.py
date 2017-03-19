import unittest

from biblia import Main


class Test(unittest.TestCase):
    def test_asd(self):
        m = Main()
        m.fitting('i')
