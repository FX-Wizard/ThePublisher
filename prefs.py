import os
from configparser import ConfigParser


class UserPrefs():
    def __init__(self):
        # create preference directory if not exists
        HOME_DIR = os.path.expanduser('~')
        CONFIG_DIR = os.path.join(HOME_DIR, 'publisher')
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        
        CONFIG_FILE = os.path.join(CONFIG_DIR, 'user-prefs.ini')
        self.data = INIHandler(CONFIG_FILE)
        if not os.path.exists(CONFIG_FILE):
            self.createConfigFile()

    def createConfigFile(self):
        self.data['previous_selection'] = {
            'project_name': '',
        }
        self.data.save()


class INIHandler():
    def __init__(self, fileName):
        '''opens and parses .ini files and saves them out again'''
        self.fileName = fileName
        self.config = ConfigParser(dict_type=AttrDict)
        if os.path.exists(self.fileName):
            try:
                self.config.read(self.fileName)
            except:
                raise('error reading file')

    @property
    def data(self):
        return self.config._sections

    def __getitem__(self, item):
        try:
            return self.config._sections[item]
        except KeyError:
            return ''

    def __setitem__(self, key, value):
        self.config._sections[key] = value
        self.save()

    @data.setter
    def data(self, key, value):
        self.config._sections[key] = value
        self.save()

    @data.getter
    def data(self):
        return self.config._sections

    def save(self):
        '''saves out .ini file'''
        self.config.read_dict(self.data)
        try:
            with open(self.fileName, 'w') as f:
                self.config.write(f)
        except Exception as error:
            print(error)
            raise(error)


class AttrDict(dict):
    '''converts .ini file into python dict'''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)