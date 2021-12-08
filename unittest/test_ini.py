import unittest
import os

import prefs

CONFIG_FILE = 'test.ini'

class TestIniHandeler(unittest.TestCase):
    def test_createIniFile(self):
        config = prefs.INIHandler(CONFIG_FILE)
        config.save()
        self.assertTrue(os.path.isfile(CONFIG_FILE))

    def test_createSection(self):
        config = prefs.INIHandler(CONFIG_FILE)
        config['testSection'] = {}
        # config.save()

    def test_readSection(self):
        config = prefs.INIHandler(CONFIG_FILE)
        self.assertEquals(config['testSection'], {})

    def test_addDataToSection(self):
        config = prefs.INIHandler(CONFIG_FILE)
        config['testSection2'] = {'test-key': 'test-value'}

    def test_readDataFromSection(self):
        config = prefs.INIHandler(CONFIG_FILE)
        self.assertEquals(config['testSection2']['test-key'], 'test-value')


if __name__ == '__main__':
    unittest.main()