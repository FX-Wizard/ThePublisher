import os
import platform

from prefs import INIHandler
data = INIHandler('prefs.ini').data

if platform.system() == 'Windows':
    # WINDOWS
    jobsDir = data['projectDir']['win']
elif platform.system() == 'Darwin':
    # MACOS
    jobsDir = data['projectDir']['mac']
else:
    # LINUX
    jobsDir = data['projectDir']['linux']


## POPULATE COMBO BOXES ###
def populateProjects():
    '''Retrun list of projects in projects directory
    Parameters:
    Returns:
        projects (list) list of projects
    '''
    projects = []
    prefix = data['projectDir']['prefix']
    
    if not os.path.exists(jobsDir):
        return ''

    for project in os.listdir(jobsDir):
        if project.startswith(tuple(prefix)):
            projects.append(project)
    projects.sort()
    return projects


def populateRenderDir(selectedProject):
    ''' Retrun list renders from a given project
    Parameters:
        selectedProject (str) path to project
    Returns:
        renders (list) list of renders
    '''
    renderDir = data['projectMap']['render_dir']
    projectRenders = os.path.join(jobsDir, selectedProject, renderDir)

    if os.path.exists(projectRenders):
        renders = os.listdir(projectRenders)
        full_render_path = [os.path.join(projectRenders, i) for i in renders]
        full_render_sorted = sorted(full_render_path, key=os.path.getmtime, reverse=True)
        renders = [os.path.basename(r) for r in full_render_sorted]
        return renders
    else:
        return ''

def populateSequence(selectedProject):
    ''' Retrun list Sequence from a given project
    Parameters:
        selectedProject (str) path to project
    Returns:
        renders (list) list of sequences in project
    '''
    sequenceDir = data['projectMap']['sequence_dir']
    projectSequence = os.path.join(jobsDir, selectedProject, sequenceDir)
    
    if os.path.exists(projectSequence):
        sequence = os.listdir(projectSequence)
        if '.DS_Store' in sequence:
            sequence.remove('.DS_Store')
        return sequence
    else:
        return ''

def populateShots(selectedSequence):
    sequenceDir = data['projectMap']['sequence_dir']
    shotDir = os.path.join(sequenceDir, selectedSequence)
    if os.path.exists(shotDir):
        return os.listdir(shotDir)
    else:
        return ''

def renderExist(renderPath, selectedRender):
    ''' 
    get render path
    Parameters:
        renderPath (str) path to renders dir
        selectedRender (str) path to selected render
     Returns:
        path to render
    '''  
    renderOutput = os.path.join(renderPath, selectedRender)

    if os.path.exists(os.path.join(renderOutput, 'masterLayer')):
        renderOutput = os.path.join(renderOutput, 'masterLayer')
    elif os.path.exists(os.path.join(renderOutput, 'masterlayer')):
        renderOutput = os.path.join(renderOutput, 'masterlayer')
    else:
        print('ERROR RENDER DOES NOT EXIST')

    return renderOutput

def outputExists(seqPath, seq, shotSeq):
    ''' 
    gets output path
    Parameters:
        seqPath (str) path to sequence dir
        seq (str) path to sequence
        shotSeq (str) path to shot
    Returns:
        path to comp output directory
    '''    
    outputPath = os.path.join(seqPath, seq, shotSeq, 'light')

    if os.path.exists(os.path.join(outputPath, 'output', 'lightRender')):
        outputPath = os.path.join(outputPath, 'output', 'lightRender')
    elif os.path.exists(os.path.join(outputPath, '_output', 'lightRender')):
        outputPath = os.path.join(outputPath, '_output', 'lightRender')
    else:
        print('ERROR OUTPUT DOES NOT EXIST')

    return outputPath

def draftRenderDir(renderPath, selectedRender, seqPath, seq, shotSeq):

    renderOutput = os.path.join(renderPath, selectedRender)
    outputPath = os.path.join(seqPath, seq, shotSeq, 'light')

    if os.path.exists(os.path.join(renderOutput, 'masterLayer')):
        renderOutput = os.path.join(renderOutput, 'masterLayer')
    elif os.path.exists(os.path.join(renderOutput, 'masterlayer')):
        renderOutput = os.path.join(renderOutput, 'masterlayer')
    elif os.path.exists(os.path.join(outputPath, 'output', 'lightRender', selectedRender, 'masterLayer')):
        renderOutput = os.path.join(outputPath, 'output', 'lightRender', selectedRender, 'masterLayer')
    elif os.path.exists(os.path.join(outputPath, '_output', 'lightRender', selectedRender, 'masterLayer')):
        outputPath = os.path.join(outputPath, '_output', 'lightRender', selectedRender, 'masterLayer')
    else:
        print('ERROR RENDER DOES NOT EXIST')

    return renderOutput
