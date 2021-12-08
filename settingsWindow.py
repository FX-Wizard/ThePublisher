import os, sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtUiTools import QUiLoader

from prefs import INIHandler
ini = INIHandler('prefs.ini')
data = ini.data


class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        uiFileName = './ui/studioSettings.ui'
        uiFile = QtCore.QFile(uiFileName)
        if not uiFile.open(QtCore.QIODevice.ReadOnly):
            print(f'Cannot open {uiFileName}: {uiFile.errorString()}')

        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()
        if not self.window:
            print(loader.errorString())

        self.window.show()

        self.lineProjectLinux = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit_project_linux')
        self.btnOpenProjectLinux = self.window.findChild(QtWidgets.QPushButton, 'btn_open_project_linux')

        self.lineProjectMac = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit_project_mac')
        self.btnOpenProjectMac = self.window.findChild(QtWidgets.QPushButton, 'btn_open_project_mac')

        self.lineProjectWin = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit_project_win')
        self.btnOpenProjectWin = self.window.findChild(QtWidgets.QPushButton, 'btn_open_project_win')

        self.lineRender = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit_render')
        self.lineSequence = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit_sequence')
        self.lineShot = self.window.findChild(QtWidgets.QLineEdit, 'lineEdit_shot')

        self.buttonBox = self.window.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        self.buttonBox.accepted.connect(self.updateSettings)
        
        self.populateSettings()


    def populateSettings(self):
        self.lineProjectLinux.setText(data.projectDir.get('linux'))
        self.lineProjectMac.setText(data.projectDir.get('mac'))
        self.lineProjectWin.setText(data.projectDir.get('win'))
        self.lineRender.setText(data.projectMap.get('render_dir'))
        self.lineSequence.setText(data.projectMap.get('sequence_dir'))
        self.lineShot.setText(data.projectMap.get('shot_dir'))


    def updateSettings(self):
        data.projectDir['linux'] = self.lineProjectLinux.text()
        data.projectDir['mac'] = self.lineProjectMac.text()
        data.projectDir['win'] = self.lineProjectWin.text()

        data.projectMap['render_dir'] = self.lineRender.text()
        data.projectMap['sequence_dir'] = self.lineSequence.text()
        data.projectMap['shot_dir'] = self.lineShot.text()

        ini.save()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # load and set stylesheet
    styleFile = QtCore.QFile('./ui/stylesheet.qss')
    styleFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(styleFile)
    app.setStyleSheet(stream.readAll())

    window = SettingsWindow()
    sys.exit(app.exec_())