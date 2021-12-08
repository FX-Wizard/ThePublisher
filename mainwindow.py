import os, sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtUiTools import QUiLoader

import prefs
import populateProjects
import buttonFunc

from settingsWindow import SettingsWindow

from prefs import UserPrefs
userPrefs = UserPrefs().data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        uiFileName = './ui/publisherGUI.ui'
        uiFile = QtCore.QFile(uiFileName)
        if not uiFile.open(QtCore.QIODevice.ReadOnly):
            print(f'Cannot open {uiFileName}: {uiFile.errorString()}')

        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()
        if not self.window:
            print(loader.errorString())

        QtGui.QFontDatabase.addApplicationFont('./fonts/Punishment-DPwE.ttf')

        self.window.show()

        # Combo boxes
        self.projectCB = self.window.findChild(QtWidgets.QComboBox, 'projectCB')
        self.populateProjects()
        self.projectCB.activated.connect(self.onProjectSelected)

        self.renderSelectCB = self.window.findChild(QtWidgets.QComboBox, 'renderSelectCB')
        self.renderSelectCB.activated.connect(self.onRenderSelected)

        self.sequenceSelectCB = self.window.findChild(QtWidgets.QComboBox, 'sequenceSelectCB')
        self.sequenceSelectCB.activated.connect(self.onSequenceSelected)

        self.shotsCB = self.window.findChild(QtWidgets.QComboBox, 'shotsCB')
        self.shotsCB.activated.connect(self.onShotSelected)

        # Buttonts
        self.exploreImgBtn = self.window.findChild(QtWidgets.QPushButton, 'exploreImgBtn')

        self.viewImgBtn = self.window.findChild(QtWidgets.QPushButton, 'viewImgBtn')
        self.viewImgBtn.clicked.connect(self.viewImgSeq)

        self.exploreOutImgBtn = self.window.findChild(QtWidgets.QPushButton, 'exploreOutImgBtn')
        self.exploreOutImgBtn.clicked.connect(self.renderOutputDir)

        self.moveRenBtn = self.window.findChild(QtWidgets.QPushButton, 'moveRenBtn')
        self.moveRenBtn.clicked.connect(self.moveRender)

        self.publishBtn = self.window.findChild(QtWidgets.QPushButton, 'publishBtn')
        self.publishBtn.clicked.connect(self.publishDraft)

        # Action menu
        self.studioSettingsBtn = self.window.findChild(QtWidgets.QAction, 'actionStudio_Settings')
        print(self.studioSettingsBtn)
        self.studioSettingsBtn.triggered.connect(self.showSettingsMenu)


    def populateProjects(self):
        '''Populate projects comboBox with folders in projects dir'''
        projects = populateProjects.populateProjects()
        if not projects:
            self.showSettingsMenu()
        self.projectCB.addItems(projects)
        previousProject = userPrefs['previous_selection'].get('Job_Name')
        if previousProject:
            self.projectCB.setItemText(previousProject)


    def onProjectSelected(self, selection):
        '''Populate renders and sequence comboBox when project is selected
        '''
        jobSel = userPrefs['previous_selection'].get('project_name')
        if self.projectCB.currentText() == 'SELECT JOB' and jobSel:
            self.projectCB.setItemText(selection, jobSel)
        else:
            jobSel = self.projectCB.currentText()
        userPrefs.save()
        self.populateRenders(jobSel)
        self.populateSequenceList(jobSel)


    def populateRenders(self, project):
        '''Populate renders comboBox'''
        if self.renderSelectCB.count():
            self.renderSelectCB.clear()
        renders = populateProjects.populateRenderDir(project)
        self.renderSelectCB.addItems(renders)


    def onRenderSelected(self):
        '''Select and store selected render path'''
        renderPath = populateProjects.getImagePath()
        selectedRender = self.renderSelectCB.currentText()
        populateProjects.renderExist(renderPath, selectedRender)


    def populateSequenceList(self, project):
        '''select and store job sequence'''
        if self.sequenceSelectCB.count():
            self.sequenceSelectCB.clear()
        sequence = populateProjects.populateSequence(project)
        self.sequenceSelectCB.addItems(sequence)
        self.onSequenceSelected()


    def onSequenceSelected(self):
        '''Populate shot comboBox'''
        if self.shotsCB.count():
            self.shotsCB.clear()
        selectedSequence = self.sequenceSelectCB.currentText()
        shots = populateProjects.populateShots(selectedSequence)
        self.shotsCB.addItems(shots)


    # def populateShots(self):
    #     '''Populate shot comboBox'''
    #     if self.shotsCB.count():
    #         self.shotsCB.clear()
                

    def onShotSelected(self): # find and store render path
        '''Select and store selected render path'''
        seqPath = populateProjects.getSeqPath()
        seq = self.sequenceSelectCB.currentText()
        shotSeq = self.shotsCB.currentText()
        outputPath = os.path.join(seqPath, seq, shotSeq, 'light')


    def viewImgSeq(self):
        ''' View render using imgSeq player
        Parameters:
            renderPath (str) path to render dir
            selectedRender (str) gets selected render from renderSelectComboBox
            renderOutput (str) path to current seleted render
        Returns:
            none
        '''  
        renderPath = populateProjects.getImagePath()
        selectedRender = self.renderSelectCB.currentText()
        renderOutput = populateProjects.renderExist(renderPath, selectedRender)
        buttonFunc.viewRender(renderOutput)



    def exploreRenderDir(self):
        ''' Explore to current render directory
        Parameters:
            renderPath (str) path to render dir
            selectedRender (str) gets selected render from render SelectComboBox
            renderOutput (str) path to current seleted render
        Returns:
            none
        ''' 
        renderPath = populateProjects.getImagePath()
        selectedRender = self.renderSelectCB.currentText()
        renderOutput = populateProjects.renderExist(renderPath, selectedRender)
        buttonFunc.exploreRenderDir(renderOutput)


    def renderOutputDir(self):
        ''' Explore to current render output directory
        Parameters:
            seqPath (str) path to job seq dir
            seq (str) gets selected render from sequence SelectComboBox
            shotSeq (str) gets selected shot from sequence shot ComboBox
            outputPath (str) path to selected job output render directory
        Returns:
            none
        ''' 
        seqPath = populateProjects.getSeqPath()
        seq = self.sequenceSelectCB.currentText()
        shotSeq = self.shotsCB.currentText()
        outputPath = populateProjects.outputExists(seqPath, seq, shotSeq)
        buttonFunc.exploreRenderDir(outputPath)


    def moveRender(self):
        ''' Move renders form one directory to another
        Parameters:
            renderPath (str) path to render dir
            selectedRender (str) gets selected render from render SelectComboBox
            renderOutput (str) path to current seleted render

            seqPath (str) path to job seq dir
            seq (str) gets selected render from sequence SelectComboBox
            shotSeq (str) gets selected shot from sequence shot ComboBox
            outputPath (str) path to selected job output render directory
        Returns:
            none
        ''' 
        #get render path
        renderPath = populateProjects.getImagePath()
        selectedRender = self.renderSelectCB.currentText()
        renderOutput = os.path.join(renderPath, selectedRender)
        sourceDir = renderOutput        
        #get output path
        seqPath = populateProjects.getSeqPath()
        seq = self.sequenceSelectCB.currentText()
        shotSeq = self.shotsCB.currentText()
        outputPath = populateProjects.outputExists(seqPath, seq, shotSeq)
        destDir = outputPath
        buttonFunc.moveRenderDir(sourceDir,destDir) 

    
    def publishDraft(self):
        ''' publish .mp4 video file using ffmpeg
        Parameters:
            renderPath (str) path to render dir
            selectedRender (str) gets selected render from render SelectComboBox
            renderDir (str) path to current seleted render
            seqPath (str) path to job seq dir
            seq (str) gets selected render from sequence SelectComboBox
            shotSeq (str) gets selected shot from sequence shot ComboBox
            outputDir (str) path to selected job output render directory

            fileName (str) returns first file in render directory
            renderName (str) removes frame numbers from string
            renderExt(str) adds frame padding and img extension
            outputExt(str) desired output draft mov extension
        Returns:
            none
        ''' 
        renderPath = populateProjects.getImagePath()
        selectedRender = self.renderSelectCB.currentText()
        seqPath = populateProjects.getSeqPath()
        seq = self.sequenceSelectCB.currentText()
        shotSeq = self.shotsCB.currentText()

        renderDir = populateProjects.draftRenderDir(renderPath, selectedRender, seqPath, seq, shotSeq)

        fileName = [f for f in os.listdir(renderDir) if os.path.isfile(os.path.join(renderDir, f))][0]
        startFrame = (fileName[-8:-4])

        if fileName.endswith('.exr') == True:
            fileExt = '.exr'
        elif fileName.endswith('.png') == True:
            fileExt = '.png'
        elif fileName.endswith('.tiff') == True:
            fileExt = '.tiff'
        elif fileName.endswith('.jpg') == True:
            fileExt = '.jpg'
        else:
            pass
            
        renderName = fileName.replace('.' + startFrame + fileExt, "")
        renderExt = '.%04d' + fileExt

        outputDir = populateProjects.outputExists(seqPath, seq, shotSeq)
        outputExt = '.mp4'
        
        source = os.path.join(renderDir,  renderName + renderExt)
        output = os.path.join(outputDir,  renderName + outputExt)
        buttonFunc.ffmpegDraft(source,output,startFrame)

    
    def showSettingsMenu(self):
        dialog = SettingsWindow(parent=self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # load and set stylesheet
    styleFile = QtCore.QFile('./ui/stylesheet.qss')
    styleFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(styleFile)
    app.setStyleSheet(stream.readAll())

    window = MainWindow()
    sys.exit(app.exec_())