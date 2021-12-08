import os, subprocess, shutil, platform
import ffmpeg

# BUTTONS
# --------------------------------------------------------------------------------
def viewRender(renderDirPath):
    ''' plays renders
    Parameters:
        renderDirPath (str) path to renders
    Returns:
        None 
    '''
    pdPlayer = {
        'win': r'C:\Program Files\Pdplayer 64\pdplayer64.exe',
        'mac': 'add path here',
        'linux': 'need pd path'
    }
    djvPlayer = {
        'win': r"C:\Program Files\DJV2\bin\djv.exe",
        'mac': '/Applications/DJV2.app/Contents/MacOS/DJV2',
        'linux': '/populate/me/with/a/path'
    }

    if platform.system() == 'Windows':
        # WINDOWS
        if os.path.exists(pdPlayer['win']):
            playPDPlayer_Win(renderDirPath)
        else:
            playDJV_Win(renderDirPath)
    elif platform.system() == 'Darwin':
        # MACOS
        playDJV_Mac(renderDirPath)
    else:
        # LINUX
        playDJV_Linux(renderDirPath)


def playDJV_Mac(renderDirPath):
    player = '/Applications/DJV2.app/Contents/MacOS/DJV2'
    os.system('{} {}'.format(player, renderDirPath))


def playDJV_Win(renderDirPath):
    player = r'C:\Program Files\DJV2\bin\djv.exe'
    fileName = [f for f in os.listdir(renderDirPath) if os.path.isfile(os.path.join(renderDirPath, f))][0]
    filePath = os.path.join(renderDirPath, fileName)
    subprocess.Popen("{0} {1}".format(player, filePath))


def playDJV_Linux(renderDirPath):
    player = '/populate/me/with/a/path'
    subprocess.Popen("{0} {1}".format(player, renderDirPath))


def playPDPlayer_Win(renderDirPath):
    player = r'C:\Program Files\Pdplayer 64\pdplayer64.exe'
    subprocess.Popen('{} {}'.format(player, renderDirPath))


def exploreRenderDir(outputPath):
    ''' explores render output locations
    Parameters:
        outputPath (str) path to selected render
    Returns:
        none
    '''
    subprocess.Popen(r'explorer /,%s' % outputPath)


def moveRenderDir(sourceDir,destDir):
    ''' Moves render to comp locations
    Parameters:
        sourceDir (str) path to selected render
        destDir (str) path to output directory
    Returns:
        none
    '''
    shutil.move(sourceDir, destDir)


def ffmpegDraft(source,output,startFrame):
    '''
    Parameters:
        sourceDir (str) path to selected render
        destDir (str) path to output directory
    Returns:
        none
    '''
    imgformat = 'image2'
    frameRate = 25
    gamma = 2
    videoSize = 'hd720'
    videoCodec = 'libx264'
    quality = 10 # best 0 - 100 worst
    pixFmt = 'yuv420p'

    draft = ffmpeg.input(source, format=imgformat, start_number=startFrame, r=frameRate, gamma=gamma)
    draft = ffmpeg.filter(draft, 'scale', size=videoSize, force_original_aspect_ratio='decrease ')
    draft = ffmpeg.output(draft, output, vcodec=videoCodec, crf=quality, preset='slower', pix_fmt=pixFmt)

    draft = ffmpeg.overwrite_output(draft)
    ffmpeg.run(draft)