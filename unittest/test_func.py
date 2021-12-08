import unittest
import os

import buttonFunc

class Test(unittest.TestCase):
    def test_fileMove(self):
        source = 'test'
        dest = 'test'
        buttonFunc.moveRenderDir(source, dest)
        self.assertTrue(os.path.isdir(dest))

    def test_Basic(self):
        math = 1 + 1
        self.assertEqual(math, 2)

    def test_ffmpegDraft(self):
        pass

if __name__ == '__main__':
    unittest.main()