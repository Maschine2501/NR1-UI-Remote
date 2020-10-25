#!/usr/bin/python3
#      ____  ____  ___   __  ___   __     _   ______ ___
#     / __ )/ __ \/   | / / / / | / /    / | / / __ <  /
#    / __  / /_/ / /| |/ / / /  |/ /    /  |/ / /_/ / / 
#   / /_/ / _, _/ ___ / /_/ / /|  /    / /|  / _, _/ /  
#  /_____/_/ |_/_/  |_\____/_/ |_/    /_/ |_/_/ |_/_/   
#    __  __              ____     __          ___            
#   / / / /__ ___ ____  /  _/__  / /____ ____/ _/__ ________ 
#  / /_/ (_-</ -_) __/ _/ // _ \/ __/ -_) __/ _/ _ `/ __/ -_)
#  \____/___/\__/_/   /___/_//_/\__/\__/_/ /_/ \_,_/\__/\__/ 
#
#  For more Informations visit: https://github.com/Maschine2501/NR1-UI
#   _           __  __ ___ ___ ___  __  _ 
#  | |__ _  _  |  \/  / __|_  ) __|/  \/ |
#  | '_ \ || | | |\/| \__ \/ /|__ \ () | |
#  |_.__/\_, | |_|  |_|___/___|___/\__/|_|
#        |__/                                                                                                                                            
#________________________________________________________________________________________
#________________________________________________________________________________________
#	
#    ____                           __           
#   /  _/___ ___  ____  ____  _____/ /______   _ 
#   / // __ `__ \/ __ \/ __ \/ ___/ __/ ___/  (_)
# _/ // / / / / / /_/ / /_/ / /  / /_(__  )  _   
#/___/_/ /_/ /_/ .___/\____/_/   \__/____/  (_)  
#             /_/                                
from __future__ import unicode_literals
import requests
import os
import re
import sys
import time
import threading
import signal
import json
import pycurl
import pprint
import subprocess
import RPi.GPIO as GPIO
from time import*
from datetime import timedelta as timedelta
from threading import Thread
from socketIO_client import SocketIO
from datetime import datetime as datetime
from io import BytesIO 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ftplib import FTP
from modules.pushbutton import PushButton
from modules.rotaryencoder import RotaryEncoder
#import uuid
from ConfigurationFiles.PreConfiguration import*
sleep(2.0)
#from decimal import Decimal
#________________________________________________________________________________________
#________________________________________________________________________________________
#	
#   ______            _____                        __  _                 
#  / ____/___  ____  / __(_)___ ___  ___________ _/ /_(_)___  ____     _ 
# / /   / __ \/ __ \/ /_/ / __ `/ / / / ___/ __ `/ __/ / __ \/ __ \   (_)
#/ /___/ /_/ / / / / __/ / /_/ / /_/ / /  / /_/ / /_/ / /_/ / / / /  _   
#\____/\____/_/ /_/_/ /_/\__, /\__,_/_/   \__,_/\__/_/\____/_/ /_/  (_)  
#                       /____/
#
ScreenList = ['No-Spectrum']

if NowPlayingLayout not in ScreenList:
    NowPlayingLayout = 'No-Spectrum'

#config for timers:
oledPlayFormatRefreshTime = 1.5
oledPlayFormatRefreshLoopCount = 3
#________________________________________________________________________________________
#________________________________________________________________________________________
#   _____ __             __            __     _____       _ __  _                      
#  / ___// /_____ ______/ /_      ____/ /__  / __(_)___  (_) /_(_)___  ____  _____   _ 
#  \__ \/ __/ __ `/ ___/ __/_____/ __  / _ \/ /_/ / __ \/ / __/ / __ \/ __ \/ ___/  (_)
# ___/ / /_/ /_/ / /  / /_/_____/ /_/ /  __/ __/ / / / / / /_/ / /_/ / / / (__  )  _   
#/____/\__/\__,_/_/   \__/      \__,_/\___/_/ /_/_/ /_/_/\__/_/\____/_/ /_/____/  (_)  
#     
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

firstStart = True

if DisplayTechnology == 'spi1351':
   from luma.core.interface.serial import spi
   from luma.oled.device import ssd1351
   from modules.display1351 import*
   from ConfigurationFiles.ScreenConfig1351 import*

#if DisplayTechnology == 'i2c1306':
#    from luma.core.interface.serial import i2c
#    from luma.oled.device import ssd1306
#    from modules.display1306 import*
#    from ConfigurationFiles.ScreenConfig1306 import*

volumio_host = 'volumio.local'
volumio_port = 3000
volumioIO = SocketIO(volumio_host, volumio_port)
VOLUME_DT = 5

b_obj = BytesIO() 
crl = pycurl.Curl() 

ftp = FTP('volumio.local')
ftpUsername = 'volumio'
ftpPassword = 'volumio'
ftp.login('volumio', 'volumio') #(user='volumio', passwd='volumio')

STATE_NONE = -1
STATE_PLAYER = 0
STATE_QUEUE_MENU = 1
STATE_LIBRARY_INFO = 2
STATE_VOLUME = 3
#STATE_SCREEN_MENU = 3

UPDATE_INTERVAL = 0.034

if DisplayTechnology == 'spi1351':
    interface = spi(device=0, port=0)
    oled = ssd1351(interface, rotate=oledrotation) 
    oled.WIDTH = 128
    oled.HEIGHT = 128
#if DisplayTechnology == 'i2c1306':
#    interface = i2c(port=1, address=0x3C)
#    oled = ssd1306(interface) #, rotate=oledrotation)
#    oled.WIDTH = 128
#    oled.HEIGHT = 64 

oled.state = 'stop'
oled.stateTimeout = 0
oled.playstateIcon = ''
oled.timeOutRunning = False
oled.activeSong = ''
oled.activeArtist = 'VOLuMIO'
oled.playState = 'unknown'
oled.playPosition = 0
oled.seek = 1000
oled.duration = 1.0
oled.modal = False
oled.playlistoptions = []
oled.queue = []
oled.libraryFull = []
oled.libraryNames = []
oled.volumeControlDisabled = True
oled.volume = 100
now = datetime.now()                       #current date and time
oled.time = now.strftime("%H:%M:%S")       #resolves time as HH:MM:SS eg. 14:33:15
oled.date = now.strftime("%d.%m.%Y")   #resolves time as dd.mm.YYYY eg. 17.04.2020
oled.IP = ''
emit_track = False
newStatus = 0              				   #makes newStatus usable outside of onPushState
oled.activeFormat = ''      			   #makes oled.activeFormat globaly usable
oled.activeSamplerate = ''  			   #makes oled.activeSamplerate globaly usable
oled.activeBitdepth = ''                   #makes oled.activeBitdepth globaly usable
oled.activeArtists = ''                    #makes oled.activeArtists globaly usable
oled.activeAlbumArt = ''
oled.activeAlbums = ''                     #makes oled.activeAlbums globaly usable
oled.activeAlbum = ''
oled.activeSongs = ''                      #makes oled.activeSongs globaly usable
oled.activePlaytime = ''                   #makes oled.activePlaytime globaly usable
oled.randomTag = False                     #helper to detect if "Random/shuffle" is set
oled.repeatTag = False                     #helper to detect if "repeat" is set
oled.ShutdownFlag = False                  #helper to detect if "shutdown" is running. Prevents artifacts from Standby-Screen during shutdown
varcanc = True                      #helper for pause -> stop timeout counter
secvar = 0.0
oled.volume = 100
oled.SelectedScreen = NowPlayingLayout
oled.fallingL = False
oled.fallingR = False
oled.prevFallingTimerL = 0
oled.prevFallingTimerR = 0
ScrollArtistTag = 0
ScrollArtistNext = 0
ScrollArtistFirstRound = True
ScrollArtistNextRound = False
ScrollSongTag = 0
ScrollSongNext = 0
ScrollSongFirstRound = True
ScrollSongNextRound = False
ScrollAlbumTag = 0
ScrollAlbumNext = 0
ScrollAlbumFirstRound = True
ScrollAlbumNextRound = False
oled.selQueue = ''
oled.volumeControlDisabled = False
oled.volume = 100
emit_volume = False
emit_track = False
oled.ScreenTimer10 = False
oled.ScreenTimer20 = False
oled.ScreenTimerStamp = 0.0
oled.ScreenTimerStart = True
oled.ScreenTimerChangeTime = 10.0

if DisplayTechnology != 'i2c1306':
    image = Image.new('RGB', (oled.WIDTH, oled.HEIGHT))  #for Pixelshift: (oled.WIDTH + 4, oled.HEIGHT + 4)) 
#if DisplayTechnology == 'i2c1306':
#    image = Image.new('1', (oled.WIDTH, oled.HEIGHT))  #for Pixelshift: (oled.WIDTH + 4, oled.HEIGHT + 4))  
oled.clear()
#________________________________________________________________________________________
#________________________________________________________________________________________
#	
#    ______            __           
#   / ____/___  ____  / /______   _ 
#  / /_  / __ \/ __ \/ __/ ___/  (_)
# / __/ / /_/ / / / / /_(__  )  _   
#/_/    \____/_/ /_/\__/____/  (_)  
#
#if DisplayTechnology != 'i2c1306':  
#    font = load_font('Oxanium-Bold.ttf', 18)                       #used for Artist ('Oxanium-Bold.ttf', 20)  
#    font2 = load_font('Oxanium-Light.ttf', 12)                     #used for all menus
#    font3 = load_font('Oxanium-Regular.ttf', 16)                   #used for Song ('Oxanium-Regular.ttf', 18) 
#    font4 = load_font('Oxanium-Medium.ttf', 12)                    #used for Format/Smplerate/Bitdepth
#    font5 = load_font('Oxanium-Medium.ttf', 12)                    #used for Artist / Screen5
#    font6 = load_font('Oxanium-Regular.ttf', 12)                   #used for Song / Screen5
#    font7 = load_font('Oxanium-Light.ttf', 10)                     #used for all other / Screen5
#    font8 = load_font('Oxanium-Regular.ttf', 10)                   #used for Song / Screen5
#    font9 = load_font('Oxanium-Bold.ttf', 16)                       #used for Artist ('Oxanium-Bold.ttf', 20)  
#    font10 = load_font('Oxanium-Regular.ttf', 14)                       #used for Artist ('Oxanium-Bold.ttf', 20)  
#    mediaicon = load_font('fa-solid-900.ttf', 10)    	           #used for icon in Media-library info
#    iconfont = load_font('entypo.ttf', oled.HEIGHT)                #used for play/pause/stop/shuffle/repeat... icons
#    labelfont = load_font('entypo.ttf', 12)                        #used for Menu-icons
#    iconfontBottom = load_font('entypo.ttf', 10)                   #used for icons under the screen / button layout
#    fontClock = load_font('DSG.ttf', 30)                           #used for clock
#    fontDate = load_font('Oxanium-Light.ttf', 12)           #used for Date 'DSEG7Classic-Regular.ttf'
#    fontIP = load_font('Oxanium-Light.ttf', 12)             #used for IP 'DSEG7Classic-Regular.ttf'
if DisplayTechnology == 'spi1351':
    font = load_font('Oxanium-Bold.ttf', 16)                       #used for Artist
    font2 = load_font('Oxanium-Light.ttf', 12)                     #used for all menus
    font3 = load_font('Oxanium-Regular.ttf', 14)                   #used for Song
    font4 = load_font('Oxanium-Medium.ttf', 12)                    #used for Format/Smplerate/Bitdepth
    font5 = load_font('Oxanium-Medium.ttf', 14)                    #used for Album
    mediaicon = load_font('fa-solid-900.ttf', 10)    	           #used for icon in Media-library info
    iconfont = load_font('entypo.ttf', oled.HEIGHT)                #used for play/pause/stop/shuffle/repeat... icons
    labelfont = load_font('entypo.ttf', 12)                        #used for Menu-icons
    iconfontBottom = load_font('entypo.ttf', 10)                   #used for icons under the screen / button layout
    fontClock = load_font('DSG.ttf', 24)                           #used for clock
    fontDate = load_font('Oxanium-Medium.ttf', 12)           #used for Date 
    fontIP = load_font('Oxanium-Medium.ttf', 12)             #used for IP      
#above are the "imports" for the fonts. 
#After the name of the font comes a number, this defines the Size (height) of the letters. 
#Just put .ttf file in the 'Volumio-OledUI/fonts' directory and make an import like above. 
#________________________________________________________________________________________
#________________________________________________________________________________________
#
#    ________        ___       __                        
#   /  _/ __ \      /   | ____/ /_______  __________   _ 
#   / // /_/ /_____/ /| |/ __  / ___/ _ \/ ___/ ___/  (_)
# _/ // ____/_____/ ___ / /_/ / /  /  __(__  |__  )  _   
#/___/_/         /_/  |_\__,_/_/   \___/____/____/  (_)  
#   
def GetIP():
    wanip = GetWLANIP()
    WLANip = str(wanip.decode('ascii'))
    print('Wifi IP: ', WLANip)
    if WLANip != '':
       ip = WLANip
    else:
       ip = "no ip"
    oled.IP = ip

def GetWLANIP():
    cmd = \
        "ip addr show wlan0 | grep inet  | grep -v inet6 | awk '{print $2}' | cut -d '/' -f 1"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    return output[:-1]
#________________________________________________________________________________________
#________________________________________________________________________________________
#    ____              __        __  __          
#   / __ )____  ____  / /_      / / / /___     _ 
#  / __  / __ \/ __ \/ __/_____/ / / / __ \   (_)
# / /_/ / /_/ / /_/ / /_/_____/ /_/ / /_/ /  _   
#/_____/\____/\____/\__/      \____/ .___/  (_)  
#                                 /_/            
#
GetIP()
#________________________________________________________________________________________
#________________________________________________________________________________________
#
#    ____  _            __                  __  __          __      __           
#   / __ \(_)________  / /___ ___  __      / / / /___  ____/ /___ _/ /____     _ 
#  / / / / / ___/ __ \/ / __ `/ / / /_____/ / / / __ \/ __  / __ `/ __/ _ \   (_)
# / /_/ / (__  ) /_/ / / /_/ / /_/ /_____/ /_/ / /_/ / /_/ / /_/ / /_/  __/  _   
#/_____/_/____/ .___/_/\__,_/\__, /      \____/ .___/\__,_/\__,_/\__/\___/  (_)  
#            /_/            /____/           /_/                                 
#
def display_update_service():
    while UPDATE_INTERVAL > 0 and oled.ShutdownFlag == False:
        prevTime = time()
        dt = (time() - prevTime) * 1000
        #print('dt: ', dt)
        if oled.stateTimeout > 0:
            oled.timeOutRunning = True
            oled.stateTimeout -= dt
        elif oled.stateTimeout <= 0 and oled.timeOutRunning:
            oled.timeOutRunning = False
            oled.stateTimeout = 0
            SetState(STATE_PLAYER)
            if oled.playState != 'stop':
                oled.modal.UpdatePlayingInfo()
            if oled.playState == 'stop':
                oled.modal.UpdateStandbyInfo()
        image.paste("black", [0, 0, image.size[0], image.size[1]])
        try:
            oled.modal.DrawOn(image)
        except AttributeError:
            print("render error")
            sleep(1) 
        cimg = image.crop((0, 0, oled.WIDTH, oled.HEIGHT)) 
        oled.display(cimg)
        sleep(UPDATE_INTERVAL)
#________________________________________________________________________________________
#________________________________________________________________________________________
#
#   ____  __      _           __ _           
#  / __ \/ /_    (_)__  _____/ /( )_____   _ 
# / / / / __ \  / / _ \/ ___/ __/// ___/  (_)
#/ /_/ / /_/ / / /  __/ /__/ /_  (__  )  _   
#\____/_.___/_/ /\___/\___/\__/ /____/  (_)  
#          /___/                             
#
def SetState(status):
    oled.state = status
    if oled.state == STATE_PLAYER:
        oled.modal = NowPlayingScreen(oled.HEIGHT, oled.WIDTH) 
    elif oled.state == STATE_QUEUE_MENU:
        oled.modal = MenuScreen(oled.HEIGHT, oled.WIDTH)
    elif oled.state == STATE_LIBRARY_INFO:
        oled.modal = MediaLibrarayInfo(oled.HEIGHT, oled.WIDTH)
    elif oled.state == STATE_VOLUME:
        oled.modal = VolumeScreen(oled.HEIGHT, oled.WIDTH, oled.volume)
    #elif oled.state == STATE_SCREEN_MENU:
    #    oled.modal = ScreenSelectMenu(oled.HEIGHT, oled.WIDTH)

#________________________________________________________________________________________
#________________________________________________________________________________________
#        
#    ____        __              __  __                ____              
#   / __ \____ _/ /_____ _      / / / /___ _____  ____/ / /__  _____   _ 
#  / / / / __ `/ __/ __ `/_____/ /_/ / __ `/ __ \/ __  / / _ \/ ___/  (_)
# / /_/ / /_/ / /_/ /_/ /_____/ __  / /_/ / / / / /_/ / /  __/ /     _   
#/_____/\__,_/\__/\__,_/     /_/ /_/\__,_/_/ /_/\__,_/_/\___/_/     (_)  
#   
def grabAlbumart():
    sleep(1.0)
    #ftp.login('volumio', 'volumio') #(user='volumio', passwd='volumio')
    destinationFile = '/home/pi/album.bmp'
    filename = 'album.bmp'
    with open(destinationFile, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)
    #ftp.quit()
    #localfile = open(filename, 'wb')
    #ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    #ftp.quit()
    #localfile.close()

def onPushState(data):
    #print('onPushState')
#        data = json.loads(data.decode("utf-8"))
    global OPDsave	
    global newStatus #global definition for newStatus, used at the end-loop to update standby
    global newSong
    global newArtist
    global newFormat
    global varcanc
    global secvar
    global ScrollArtistTag
    global ScrollArtistNext
    global ScrollArtistFirstRound
    global ScrollArtistNextRound                  
    global ScrollSongTag
    global ScrollSongNext
    global ScrollSongFirstRound
    global ScrollSongNextRound
    OPDsave = data
#       print('data: ', str(data).encode('utf-8'))    

    if 'title' in data:
        newSong = data['title']
    else:
        newSong = ''
    if newSong is None:
        newSong = ''
    if newSong == 'HiFiBerry ADC':
        newSong = 'Bluetooth-Audio'
        
    if 'artist' in data:
        newArtist = data['artist']
    else:
        newArtist = ''
    if newArtist is None and newSong != 'HiFiBerry ADC':   #volumio can push NoneType
        newArtist = ''
    if newArtist == '' and newSong == 'HiFiBerry ADC':
        newArtist = 'Line-Input:'
    if 'trackType' in data:
        newFormat = data['trackType']
        oled.activeFormat = newFormat
        if newFormat == True and newSong != 'HiFiBerry ADC':
            newFormat = 'WebRadio'
            oled.activeFormat = newFormat
        if newFormat == True and newSong == 'HiFiBerry ADC':
            newFormat = 'Live-Stream'
            oled.activeFormat = newFormat
           	
#       if 'stream' in data:
#           newFormat = data['stream']
#           if newFormat == False:
#               newFormat = newTrackType
#               oled.activeFormat = newFormat
#           if newFormat is None:
#               newFormat = ''
#               oled.activeFormat = newFormat
#           if newFormat == True and newSong != 'HiFiBerry ADC':
#               newFormat = 'WebRadio'
#               oled.activeFormat = newFormat
#           if newFormat == True and newSong == 'HiFiBerry ADC':
#               newFormat = 'Live-Stream'
#               oled.activeFormat = newFormat
            
	#If a stream (like webradio) is playing, the data set for 'stream'/newFormat is a boolian (True)
	#drawOn can't handle that and gives an error. 
	#therefore we use "if newFormat == True:" and define a placeholder Word, you can change it.

    if 'samplerate' in data:
        newSamplerate = data['samplerate']
        oled.activeSamplerate = newSamplerate
    else:
        newSamplerate = ' '
        oled.activeSamplerate = newSamplerate
    if newSamplerate is None:
        newSamplerate = ' '
        oled.activeSamplerate = newSamplerate

    if 'bitdepth' in data:
        newBitdepth = data['bitdepth']
        oled.activeBitdepth = newBitdepth
    else:
        newBitdepth = ' '
        oled.activeBitdepth = newBitdepth
    if newBitdepth is None:
        newBitdepth = ' '
        oled.activeBitdepth = newBitdepth  
        
    if 'position' in data:                      # current position in queue
        oled.playPosition = data['position']    # didn't work well with volumio ver. < 2.5
        
    if 'status' in data:
        newStatus = data['status']
    
    if ledActive == True and 'channels' in data:
        channels = data['channels']
        if channels == 2:
           StereoLEDon()
        else:
           StereoLEDoff()

    if 'duration' in data:
        oled.duration = data['duration']
    else:
        oled.duration = None
    if oled.duration == int(0):
        oled.duration = None

    if 'seek' in data:
        oled.seek = data['seek']
    else:
        oled.seek = None
    if newArtist is None:   #volumio can push NoneType
        newArtist = ''

    if 'albumart' in data:
        newAlbumart = data['albumart']
    if newAlbumart is None:
        newAlbumart = 'nothing'

    if 'album' in data:
        newAlbum = data['album']

    if oled.state != STATE_VOLUME:            #get volume on startup and remote control
        try:                                  #it is either number or unicode text
            oled.volume = int(data['volume'])
        except (KeyError, ValueError):
            pass
    
    if 'disableVolumeControl' in data:
        oled.volumeControlDisabled = data['disableVolumeControl']

    if (newSong != oled.activeSong) or (newArtist != oled.activeArtist) or (newAlbum != oled.activeAlbum):                                # new song and artist
        oled.activeAlbum = newAlbum
        oled.activeSong = newSong
        oled.activeArtist = newArtist
        varcanc = True                      #helper for pause -> stop timeout counter
        secvar = 0.0
        ScrollArtistTag = 0
        ScrollArtistNext = 0
        ScrollArtistFirstRound = True
        ScrollArtistNextRound = False                  
        ScrollSongTag = 0
        ScrollSongNext = 0
        ScrollSongFirstRound = True
        ScrollSongNextRound = False
        if oled.state == STATE_PLAYER and newStatus != 'stop':                                          #this is the "NowPlayingScreen"
            oled.modal.UpdatePlayingInfo()     #here is defined which "data" should be displayed in the class
        
    if newStatus != oled.playState:
        varcanc = True                      #helper for pause -> stop timeout counter
        secvar = 0.0
        oled.playState = newStatus
        if oled.state == STATE_PLAYER:
            if oled.playState != 'stop':
                if newStatus == 'pause':
                    oled.playstateIcon = oledpauseIcon
                if newStatus == 'play':
                    oled.playstateIcon = oledplayIcon
                #oled.modal.UpdatePlayingInfo()
            else:
                ScrollArtistTag = 0
                ScrollArtistNext = 0
                ScrollArtistFirstRound = True
                ScrollArtistNextRound = False                  
                ScrollSongTag = 0
                ScrollSongNext = 0
                ScrollSongFirstRound = True
                ScrollSongNextRound = False
                #SetState(STATE_PLAYER)
                oled.modal.UpdateStandbyInfo()

    if (newAlbumart != oled.activeAlbumArt):
        oled.activeAlbumArt = newAlbumart
        grabAlbumart()

def onPushCollectionStats(data):
    data = json.loads(data.decode("utf-8"))             #data import from REST-API (is set when ButtonD short-pressed in Standby)

    if "artists" in data:               #used for Media-Library-Infoscreen
        newArtists = data["artists"]
    else:
        newArtists = ''
    if newArtists is None:
        newArtists = ''

    if 'albums' in data:                #used for Media-Library-Infoscreen
        newAlbums = data["albums"]
    else:
        newAlbums = ''
    if newAlbums is None:
        newAlbums = ''

    if 'songs' in data:                 #used for Media-Library-Infoscreen
        newSongs = data["songs"]
    else:
        newSongs = ''
    if newSongs is None:
        newSongs = ''

    if 'playtime' in data:               #used for Media-Library-Infoscreen
        newPlaytime = data["playtime"]
    else:
        newPlaytime = ''
    if newPlaytime is None:
        newPlaytime = ''

    oled.activeArtists = str(newArtists) 
    oled.activeAlbums = str(newAlbums)
    oled.activeSongs = str(newSongs)
    oled.activePlaytime = str(newPlaytime)
	
    if oled.state == STATE_LIBRARY_INFO and oled.playState == 'info':                                   #this is the "Media-Library-Info-Screen"
       oled.modal.UpdateLibraryInfo() 

def onPushQueue(data):
    print('onPushQueue')
    oled.queue = [track['name'] if 'name' in track else 'no track' for track in data]
#________________________________________________________________________________________
#________________________________________________________________________________________
#	
#    ____  _            __                  __  ___                _           
#   / __ \(_)________  / /___ ___  __      /  |/  /__  ____  __  _( )_____   _ 
#  / / / / / ___/ __ \/ / __ `/ / / /_____/ /|_/ / _ \/ __ \/ / / /// ___/  (_)
# / /_/ / (__  ) /_/ / / /_/ / /_/ /_____/ /  / /  __/ / / / /_/ / (__  )  _   
#/_____/_/____/ .___/_/\__,_/\__, /     /_/  /_/\___/_/ /_/\__,_/ /____/  (_)  
#            /_/            /____/                                             
#
class NowPlayingScreen():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        #self.alfaimage = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
    def UpdatePlayingInfo(self):
        if DisplayTechnology != 'i2c1306': 
            self.image = Image.new('RGB', (self.width, self.height))
            self.draw = ImageDraw.Draw(self.image)
            
        #if DisplayTechnology == 'i2c1306':
        #    self.image = Image.new('1', (self.width, self.height))
        #    self.draw = ImageDraw.Draw(self.image)
        
    def UpdateStandbyInfo(self):
        if DisplayTechnology != 'i2c1306': 
            self.image = Image.new('RGB', (self.width, self.height))
            self.draw = ImageDraw.Draw(self.image)
            
        #if DisplayTechnology == 'i2c1306':
        #    self.image = Image.new('1', (self.width, self.height))
        #    self.draw = ImageDraw.Draw(self.image)

    def DrawOn(self, image):
        global ScrollArtistTag
        global ScrollArtistNext
        global ScrollArtistFirstRound
        global ScrollArtistNextRound
        global ScrollSongTag
        global ScrollSongNext
        global ScrollSongFirstRound
        global ScrollSongNextRound
        global ScrollAlbumTag
        global ScrollAlbumNext
        global ScrollAlbumFirstRound
        global ScrollAlbumNextRound

        if NowPlayingLayout == 'No-Spectrum' and newStatus != 'stop' and oled.ScreenTimer10 == True:

            if newStatus != 'stop' and oled.duration != None:
                self.image.paste(('black'), [0, 0, image.size[0], image.size[1]])
                self.playbackPoint = oled.seek / oled.duration / 10
                self.bar = Screen1barwidth * self.playbackPoint / 100
                self.ArtistWidth, self.ArtistHeight = self.draw.textsize(oled.activeArtist, font=font)
                self.ArtistStopPosition = self.ArtistWidth - self.width + ArtistEndScrollMargin
                if self.ArtistWidth >= self.width:
                    if ScrollArtistFirstRound == True:
                        ScrollArtistFirstRound = False
                        ScrollArtistTag = 0
                        self.ArtistPosition = (Screen1text01)
                    elif ScrollArtistFirstRound == False and ScrollArtistNextRound == False:
                        if ScrollArtistTag <= self.ArtistWidth - 1:
                            ScrollArtistTag += ArtistScrollSpeed
                            self.ArtistPosition = (-ScrollArtistTag ,Screen1text01[1])
                            ScrollArtistNext = 0
                        elif ScrollArtistTag == self.ArtistWidth:
                            ScrollArtistTag = 0
                            ScrollArtistNextRound = True
                            ScrollArtistNext = self.width + ArtistEndScrollMargin
                    if ScrollArtistNextRound == True:        
                        if ScrollArtistNext >= 0:                    
                            self.ArtistPosition = (ScrollArtistNext ,Screen1text01[1])
                            ScrollArtistNext -= ArtistScrollSpeed
                        elif ScrollArtistNext == -ArtistScrollSpeed and ScrollArtistNextRound == True:
                            ScrollArtistNext = 0
                            ScrollArtistNextRound = False
                            ScrollArtistFirstRound = False
                            ScrollArtistTag = 0
                            self.ArtistPosition = (Screen1text01)
                if self.ArtistWidth <= self.width:                  # center text
                    self.ArtistPosition = (int((self.width-self.ArtistWidth)/2), Screen1text01[1])  
                self.draw.text((self.ArtistPosition), oled.activeArtist, font=font, fill='white')

                self.AlbumWidth, self.AlbumHeight = self.draw.textsize(oled.activeAlbum, font=font3)
                self.AlbumStopPosition = self.AlbumWidth - self.width + AlbumEndScrollMargin
                if self.AlbumWidth >= self.width:
                    if ScrollAlbumFirstRound == True:
                        ScrollAlbumFirstRound = False
                        ScrollAlbumTag = 0
                        self.AlbumPosition = (Screen1text09)
                    elif ScrollAlbumFirstRound == False and ScrollAlbumNextRound == False:
                        if ScrollAlbumTag <= self.AlbumWidth - 1:
                            ScrollAlbumTag += AlbumScrollSpeed
                            self.AlbumPosition = (-ScrollAlbumTag ,Screen1text09[1])
                            ScrollAlbumNext = 0
                        elif ScrollAlbumTag == self.AlbumWidth:
                            ScrollAlbumTag = 0
                            ScrollAlbumNextRound = True
                            ScrollAlbumNext = self.width + AlbumEndScrollMargin
                    if ScrollAlbumNextRound == True:        
                        if ScrollAlbumNext >= 0:                    
                            self.AlbumPosition = (ScrollAlbumNext ,Screen1text09[1])
                            ScrollAlbumNext -= AlbumScrollSpeed
                        elif ScrollAlbumNext == -AlbumScrollSpeed and ScrollAlbumNextRound == True:
                            ScrollAlbumNext = 0
                            ScrollAlbumNextRound = False
                            ScrollAlbumFirstRound = False
                            ScrollAlbumTag = 0
                            self.AlbumPosition = (Screen1text09)
                if self.AlbumWidth <= self.width:                  # center text
                    self.AlbumPosition = (int((self.width-self.AlbumWidth)/2), Screen1text09[1])  
                self.draw.text((self.AlbumPosition), oled.activeAlbum, font=font3, fill=(0, 255, 0))

                self.SongWidth, self.SongHeight = self.draw.textsize(oled.activeSong, font=font5)
                self.SongStopPosition = self.SongWidth - self.width + SongEndScrollMargin
                if self.SongWidth >= self.width:
                    if ScrollSongFirstRound == True:
                        ScrollSongFirstRound = False
                        ScrollSongTag = 0
                        self.SongPosition = (Screen1text02)
                    elif ScrollSongFirstRound == False and ScrollSongNextRound == False:
                        if ScrollSongTag <= self.SongWidth - 1:
                            ScrollSongTag += SongScrollSpeed
                            self.SongPosition = (-ScrollSongTag ,Screen1text02[1])
                            ScrollSongNext = 0
                        elif ScrollSongTag == self.SongWidth:
                            ScrollSongTag = 0
                            ScrollSongNextRound = True
                            ScrollSongNext = self.width + SongEndScrollMargin
                    if ScrollSongNextRound == True:        
                        if ScrollSongNext >= 0:                    
                            self.SongPosition = (ScrollSongNext ,Screen1text02[1])
                            ScrollSongNext -= SongScrollSpeed
                        elif ScrollSongNext == -SongScrollSpeed and ScrollSongNextRound == True:
                            ScrollSongNext = 0
                            ScrollSongNextRound = False
                            ScrollSongFirstRound = False
                            ScrollSongTag = 0
                            self.SongPosition = (Screen1text02)
                if self.SongWidth <= self.width:                  # center text
                    self.SongPosition = (int((self.width-self.SongWidth)/2), Screen1text02[1])  
                self.draw.text((self.SongPosition), oled.activeSong, font=font5, fill='white')
                self.draw.text((Screen1text28), oled.playstateIcon, font=labelfont, fill=(0, 255, 0))
                self.draw.text((Screen1text06), oled.activeFormat, font=font4, fill=(0, 255, 0))
                self.draw.text((Screen1text07), str(oled.activeSamplerate), font=font4, fill=(0, 255, 0))
                self.draw.text((Screen1text08), oled.activeBitdepth, font=font4, fill=(0, 255, 0))
                self.draw.text((Screen1ActualPlaytimeText), str(timedelta(seconds=round(float(oled.seek) / 1000))), font=font4, fill='white')
                self.draw.text((Screen1DurationText), str(timedelta(seconds=oled.duration)), font=font4, fill='white')
                self.draw.rectangle((Screen1barLineX , Screen1barLineThick1, Screen1barLineX+Screen1barwidth, Screen1barLineThick2), outline=Screen1barLineBorder, fill=Screen1barLineFill)
                self.draw.rectangle((self.bar+Screen1barLineX-Screen1barNibbleWidth, Screen1barThick1, Screen1barX+self.bar+Screen1barNibbleWidth, Screen1barThick2), outline=Screen1barBorder, fill=Screen1barFill)          
                image.paste(self.image, (0, 0))

            if newStatus != 'stop' and oled.duration == None:
                self.image.paste(('black'), [0, 0, image.size[0], image.size[1]])
                self.ArtistWidth, self.ArtistHeight = self.draw.textsize(oled.activeArtist, font=font)
                self.ArtistStopPosition = self.ArtistWidth - self.width + ArtistEndScrollMargin
                if self.ArtistWidth >= self.width:
                    if ScrollArtistFirstRound == True:
                        ScrollArtistFirstRound = False
                        ScrollArtistTag = 0
                        self.ArtistPosition = (Screen1text01)
                    elif ScrollArtistFirstRound == False and ScrollArtistNextRound == False:
                        if ScrollArtistTag <= self.ArtistWidth - 1:
                            ScrollArtistTag += ArtistScrollSpeed
                            self.ArtistPosition = (-ScrollArtistTag ,Screen1text01[1])
                            ScrollArtistNext = 0
                        elif ScrollArtistTag == self.ArtistWidth:
                            ScrollArtistTag = 0
                            ScrollArtistNextRound = True
                            ScrollArtistNext = self.width + ArtistEndScrollMargin
                    if ScrollArtistNextRound == True:        
                        if ScrollArtistNext >= 0:                    
                            self.ArtistPosition = (ScrollArtistNext ,Screen1text01[1])
                            ScrollArtistNext -= ArtistScrollSpeed
                        elif ScrollArtistNext == -ArtistScrollSpeed and ScrollArtistNextRound == True:
                            ScrollArtistNext = 0
                            ScrollArtistNextRound = False
                            ScrollArtistFirstRound = False
                            ScrollArtistTag = 0
                            self.ArtistPosition = (Screen1text01)
                if self.ArtistWidth <= self.width:                  # center text
                    self.ArtistPosition = (int((self.width-self.ArtistWidth)/2), Screen1text01[1])  
                self.draw.text((self.ArtistPosition), oled.activeArtist, font=font, fill='white')

                self.AlbumWidth, self.AlbumHeight = self.draw.textsize(oled.activeAlbum, font=font)
                self.AlbumStopPosition = self.AlbumWidth - self.width + AlbumEndScrollMargin
                if self.AlbumWidth >= self.width:
                    if ScrollAlbumFirstRound == True:
                        ScrollAlbumFirstRound = False
                        ScrollAlbumTag = 0
                        self.AlbumPosition = (Screen1text09)
                    elif ScrollAlbumFirstRound == False and ScrollAlbumNextRound == False:
                        if ScrollAlbumTag <= self.AlbumWidth - 1:
                            ScrollAlbumTag += AlbumScrollSpeed
                            self.AlbumPosition = (-ScrollAlbumTag ,Screen1text09[1])
                            ScrollAlbumNext = 0
                        elif ScrollAlbumTag == self.AlbumWidth:
                            ScrollAlbumTag = 0
                            ScrollAlbumNextRound = True
                            ScrollAlbumNext = self.width + AlbumEndScrollMargin
                    if ScrollAlbumNextRound == True:        
                        if ScrollAlbumNext >= 0:                    
                            self.AlbumPosition = (ScrollAlbumNext ,Screen1text09[1])
                            ScrollAlbumNext -= AlbumScrollSpeed
                        elif ScrollAlbumNext == -AlbumScrollSpeed and ScrollAlbumNextRound == True:
                            ScrollAlbumNext = 0
                            ScrollAlbumNextRound = False
                            ScrollAlbumFirstRound = False
                            ScrollAlbumTag = 0
                            self.AlbumPosition = (Screen1text09)
                if self.AlbumWidth <= self.width:                  # center text
                    self.AlbumPosition = (int((self.width-self.AlbumWidth)/2), Screen1text09[1])  
                self.draw.text((self.AlbumPosition), oled.activeAlbum, font=font, fill=(0, 255, 0))

                self.SongWidth, self.SongHeight = self.draw.textsize(oled.activeSong, font=font3)
                self.SongStopPosition = self.SongWidth - self.width + SongEndScrollMargin
                if self.SongWidth >= self.width:
                    if ScrollSongFirstRound == True:
                        ScrollSongFirstRound = False
                        ScrollSongTag = 0
                        self.SongPosition = (Screen1text02)
                    elif ScrollSongFirstRound == False and ScrollSongNextRound == False:
                        if ScrollSongTag <= self.SongWidth - 1:
                            ScrollSongTag += SongScrollSpeed
                            self.SongPosition = (-ScrollSongTag ,Screen1text02[1])
                            ScrollSongNext = 0
                        elif ScrollSongTag == self.SongWidth:
                            ScrollSongTag = 0
                            ScrollSongNextRound = True
                            ScrollSongNext = self.width + SongEndScrollMargin
                    if ScrollSongNextRound == True:        
                        if ScrollSongNext >= 0:                    
                            self.SongPosition = (ScrollSongNext ,Screen1text02[1])
                            ScrollSongNext -= SongScrollSpeed
                        elif ScrollSongNext == -SongScrollSpeed and ScrollSongNextRound == True:
                            ScrollSongNext = 0
                            ScrollSongNextRound = False
                            ScrollSongFirstRound = False
                            ScrollSongTag = 0
                            self.SongPosition = (Screen1text02)
                if self.SongWidth <= self.width:                  # center text
                    self.SongPosition = (int((self.width-self.SongWidth)/2), Screen1text02[1])  
                self.draw.text((self.SongPosition), oled.activeSong, font=font3, fill='white')
                image.paste(self.image, (0, 0))

        if NowPlayingLayout == 'No-Spectrum' and newStatus != 'stop' and oled.ScreenTimer20 == True:

            if newStatus != 'stop' and oled.duration != None:
                self.image.paste(('black'), [0, 0, image.size[0], image.size[1]])
                self.image2 = Image.open('/home/pi/album.bmp')
                self.image.paste(self.image2, (19, 0))
                self.playbackPoint = oled.seek / oled.duration / 10
                self.bar = Screen2barwidth * self.playbackPoint / 100
                self.SongWidth, self.SongHeight = self.draw.textsize(oled.activeSong, font=font3)
                self.SongStopPosition = self.SongWidth - self.width + SongEndScrollMargin
                if self.SongWidth >= self.width:
                    if ScrollSongFirstRound == True:
                        ScrollSongFirstRound = False
                        ScrollSongTag = 0
                        self.SongPosition = (Screen2text02)
                    elif ScrollSongFirstRound == False and ScrollSongNextRound == False:
                        if ScrollSongTag <= self.SongWidth - 1:
                            ScrollSongTag += SongScrollSpeed
                            self.SongPosition = (-ScrollSongTag ,Screen2text02[1])
                            ScrollSongNext = 0
                        elif ScrollSongTag == self.SongWidth:
                            ScrollSongTag = 0
                            ScrollSongNextRound = True
                            ScrollSongNext = self.width + SongEndScrollMargin
                    if ScrollSongNextRound == True:        
                        if ScrollSongNext >= 0:                    
                            self.SongPosition = (ScrollSongNext ,Screen2text02[1])
                            ScrollSongNext -= SongScrollSpeed
                        elif ScrollSongNext == -SongScrollSpeed and ScrollSongNextRound == True:
                            ScrollSongNext = 0
                            ScrollSongNextRound = False
                            ScrollSongFirstRound = False
                            ScrollSongTag = 0
                            self.SongPosition = (Screen2text02)
                if self.SongWidth <= self.width:                  # center text
                    self.SongPosition = (int((self.width-self.SongWidth)/2), Screen2text02[1])  
                self.draw.text((self.SongPosition), oled.activeSong, font=font3, fill=(0, 255, 0))
                self.draw.text((Screen2text28), oled.playstateIcon, font=labelfont, fill=(0, 255, 0))
                self.draw.text((Screen2ActualPlaytimeText), str(timedelta(seconds=round(float(oled.seek) / 1000))), font=font4, fill='white')
                self.draw.text((Screen2DurationText), str(timedelta(seconds=oled.duration)), font=font4, fill='white')
                self.draw.rectangle((Screen2barLineX , Screen2barLineThick1, Screen2barLineX+Screen2barwidth, Screen2barLineThick2), outline=Screen2barLineBorder, fill=Screen2barLineFill)
                self.draw.rectangle((self.bar+Screen2barLineX-Screen2barNibbleWidth, Screen2barThick1, Screen2barX+self.bar+Screen2barNibbleWidth, Screen2barThick2), outline=Screen2barBorder, fill=Screen2barFill)
                image.paste(self.image, (0, 0))

            if newStatus != 'stop' and oled.duration == None:
                self.image.paste(('black'), [0, 0, image.size[0], image.size[1]])
                self.image2 = Image.open('/home/pi/album.bmp')
                self.image.paste(self.image2, (19, 0))
                self.SongWidth, self.SongHeight = self.draw.textsize(oled.activeSong, font=font3)
                self.SongStopPosition = self.SongWidth - self.width + SongEndScrollMargin
                if self.SongWidth >= self.width:
                    if ScrollSongFirstRound == True:
                        ScrollSongFirstRound = False
                        ScrollSongTag = 0
                        self.SongPosition = (Screen2text02)
                    elif ScrollSongFirstRound == False and ScrollSongNextRound == False:
                        if ScrollSongTag <= self.SongWidth - 1:
                            ScrollSongTag += SongScrollSpeed
                            self.SongPosition = (-ScrollSongTag ,Screen2text02[1])
                            ScrollSongNext = 0
                        elif ScrollSongTag == self.SongWidth:
                            ScrollSongTag = 0
                            ScrollSongNextRound = True
                            ScrollSongNext = self.width + SongEndScrollMargin
                    if ScrollSongNextRound == True:        
                        if ScrollSongNext >= 0:                    
                            self.SongPosition = (ScrollSongNext ,Screen2text02[1])
                            ScrollSongNext -= SongScrollSpeed
                        elif ScrollSongNext == -SongScrollSpeed and ScrollSongNextRound == True:
                            ScrollSongNext = 0
                            ScrollSongNextRound = False
                            ScrollSongFirstRound = False
                            ScrollSongTag = 0
                            self.SongPosition = (Screen2text02)
                if self.SongWidth <= self.width:                  # center text
                    self.SongPosition = (int((self.width-self.SongWidth)/2), Screen2text02[1])  
                self.draw.text((self.SongPosition), oled.activeSong, font=font3, fill='white')
                image.paste(self.image, (0, 0))

        elif oled.playState == 'stop':
            self.image.paste(('black'), [0, 0, image.size[0], image.size[1]])
            self.draw.text((oledtext03), oled.time, font=fontClock, fill=(0, 255, 0))
            self.draw.text((oledtext04), oled.IP, font=fontIP, fill=(0, 255, 0))
            self.draw.text((oledtext05), oled.date, font=fontDate, fill='white')
            self.draw.text((oledtext09), oledlibraryInfo, font=iconfontBottom, fill='white')
            image.paste(self.image, (0, 0))

class MediaLibrarayInfo():
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def UpdateLibraryInfo(self):
        if DisplayTechnology != 'i2c1306': 
            self.image = Image.new('RGB', (self.width, self.height))
            self.draw = ImageDraw.Draw(self.image)

    def DrawOn(self, image):
        self.image.paste(('black'), [0, 0, image.size[0], image.size[1]])
        self.draw.text((oledtext10), oled.activeArtists, font=font4, fill='white')
        self.draw.text((oledtext11), oled.activeAlbums, font=font4, fill='white')
        self.draw.text((oledtext12), oled.activeSongs, font=font4, fill='white')
        self.draw.text((oledtext13), oled.activePlaytime, font=font4, fill='white')
        self.draw.text((oledtext14), oledArt, font=font4, fill='white')
        self.draw.text((oledtext15), oledAlb, font=font4, fill='white')
        self.draw.text((oledtext16), oledSon, font=font4, fill='white')
        self.draw.text((oledtext17), oledPla, font=font4, fill='white')
        self.draw.text((oledtext19), oledlibraryReturn, font=iconfontBottom, fill='white')
        self.draw.text((oledtext20), oledArtistIcon, font=mediaicon, fill='white')
        self.draw.text((oledtext21), oledAlbumIcon, font=mediaicon, fill='white')            
        self.draw.text((oledtext22), oledSongIcon, font=mediaicon, fill='white')
        self.draw.text((oledtext23), oledPlaytimeIcon, font=mediaicon, fill='white')
        image.paste(self.image, (0, 0))

class VolumeScreen():
    def __init__(self, height, width, volume):
        self.height = height
        self.width = width
        self.volumeLabel = None
        self.labelPos = (10, 5)
        self.volumeNumber = None
        self.numberPos = (10, 25)
        self.barHeight = 6
        self.barWidth = 128
        self.volumeBar = Bar(self.height, self.width, self.barHeight, self.barWidth)
        self.barPos = (0, 64)
        self.volume = 0
        self.DisplayVolume(volume)

    def DisplayVolume(self, volume):
        self.volume = volume
        self.volumeNumber = StaticText(self.height, self.width, str(volume) + '%', font)
        self.volumeLabel = StaticText(self.height, self.width, 'Volume', font2)
        self.volumeBar.SetFilledPercentage(volume)

    def DrawOn(self, image):
        self.volumeLabel.DrawOn(image, self.labelPos)
        self.volumeNumber.DrawOn(image, self.numberPos)
        self.volumeBar.DrawOn(image, self.barPos)
        
class MenuScreen():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.selectedOption = oled.playPosition
        self.menurows = oledListEntrys
        self.menuText = [None for i in range(self.menurows)]
        self.menuList = oled.queue
        self.totaloptions = len(oled.queue)
        self.onscreenoptions = min(self.menurows, self.totaloptions)
        self.firstrowindex = 0
        self.MenuUpdate()

    def MenuUpdate(self):
        self.firstrowindex = min(self.firstrowindex, self.selectedOption)
        self.firstrowindex = max(self.firstrowindex, self.selectedOption - (self.menurows-1))
        for row in range(self.onscreenoptions):
            if (self.firstrowindex + row) == self.selectedOption:
                color = (0, 255, 0) #"black"
                bgcolor = "black" #"white"
            else:
                color = "white"
                bgcolor = "black"
            optionText = self.menuList[row+self.firstrowindex]
            self.menuText[row] = StaticText(self.height, self.width, optionText, font2, fill=color, bgcolor=bgcolor)
        if self.totaloptions == 0:
            self.menuText[0] = StaticText(self.height, self.width, oledEmptyListText, font2, fill=(0, 255, 0), bgcolor="black") #fill="white"
            
    def NextOption(self):
        self.selectedOption = min(self.selectedOption + 1, self.totaloptions - 1)
        self.MenuUpdate()

    def PrevOption(self):
        self.selectedOption = max(self.selectedOption - 1, 0)
        self.MenuUpdate()

    def SelectedOption(self):
        return self.selectedOption 

    def DrawOn(self, image):
        for row in range(self.onscreenoptions):
            self.menuText[row].DrawOn(image, (oledListTextPosX, row*oledListTextPosY))       #Here is the position of the list entrys from left set (42)
        if self.totaloptions == 0:
            self.menuText[0].DrawOn(image, (oledEmptyListTextPosition))                  #Here is the position of the list entrys from left set (42)
#________________________________________________________________________________________
#________________________________________________________________________________________
#	
#    ____        __  __                 ____                 __  _                      
#   / __ )__  __/ /_/ /_____  ____     / __/_  ______  _____/ /_(_)___  ____  _____   _ 
#  / __  / / / / __/ __/ __ \/ __ \   / /_/ / / / __ \/ ___/ __/ / __ \/ __ \/ ___/  (_)
# / /_/ / /_/ / /_/ /_/ /_/ / / / /  / __/ /_/ / / / / /__/ /_/ / /_/ / / / (__  )  _   
#/_____/\__,_/\__/\__/\____/_/ /_/  /_/  \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/  (_)  
#                                                                                       	
def ButtonA_PushEvent(hold_time):
    if hold_time < 2 and oled.state != STATE_LIBRARY_INFO:
        print('ButtonA short press event')
        if oled.state == STATE_PLAYER and oled.playState != 'stop' and newFormat != 'WebRadio':
            if oled.playState == 'play':
                volumioIO.emit('pause')
            else:
                volumioIO.emit('play')
        if oled.state == STATE_PLAYER and oled.playState != 'stop' and newFormat == 'WebRadio':
            volumioIO.emit('stop')
            oled.modal.UpdateStandbyInfo()  

def ButtonB_PushEvent(hold_time):
    if hold_time < 2 and oled.state != STATE_LIBRARY_INFO:
        print('ButtonB short press event')
        if oled.state == STATE_PLAYER and oled.playState != 'stop':
            volumioIO.emit('stop')
            oled.modal.UpdateStandbyInfo()  

def ButtonC_PushEvent(hold_time):
    if hold_time < 2:
        print('ButtonC short press event')
        #date_string = str(uuid.uuid1())
        #print(date_string)
        #image.save('/home/volumio/'+date_string+'.png')
        if oled.state == STATE_PLAYER and oled.playState != 'stop':
            volumioIO.emit('prev')
    elif oled.state == STATE_PLAYER and oled.playState != 'stop':
        print('ButtonC long press event')
        if repeatTag == False:
            volumioIO.emit('setRepeat', {"value":"true"})
            repeatTag = True            
        elif repeatTag == True:
            volumioIO.emit('setRepeat', {"value":"false"})
            repeatTag = False
       
def ButtonD_PushEvent(hold_time):
    if hold_time < 2:
        print('ButtonD short press event')
        if oled.state == STATE_PLAYER and oled.playState != 'stop':
            volumioIO.emit('next')
        if oled.state == STATE_PLAYER and oled.playState == 'stop':
            b_obj = BytesIO()
            crl = pycurl.Curl()
            crl.setopt(crl.URL, 'volumio.local:3000/api/v1/collectionstats')
            crl.setopt(crl.WRITEDATA, b_obj)
            crl.perform()
            crl.close()
            get_body = b_obj.getvalue()
            print('getBody',get_body)
            SetState(STATE_LIBRARY_INFO)
            oled.playState = 'info'
            onPushCollectionStats(get_body)
            sleep(0.5) 
        elif oled.state == STATE_LIBRARY_INFO:
            SetState(STATE_PLAYER)
    elif oled.state == STATE_PLAYER and oled.playState != 'stop':
        print('ButtonD long press event')
        if randomTag == False:
            volumioIO.emit('setRandom', {"value":"true"})
            randomTag = True
        elif randomTag == True:
            volumioIO.emit('setRandom', {"value":"false"})
            randomTag = False

def RightKnob_RotaryEvent(dir):
    global emit_volume
    if not oled.volumeControlDisabled: #and oled.state == STATE_PLAYER:
        if oled.state == STATE_PLAYER:
            #SetState(STATE_VOLUME)
            if dir == RotaryEncoder.LEFT:
                oled.volume -= VOLUME_DT
                oled.volume = max(oled.volume, 0)
                #oled.modal.DisplayVolume(oled.volume)
            elif dir == RotaryEncoder.RIGHT:
                oled.volume += VOLUME_DT
                oled.volume = min(oled.volume, 100)
                #oled.modal.DisplayVolume(oled.volume)
            oled.stateTimeout = 2.0
            if oled.state != STATE_VOLUME:
                SetState(STATE_VOLUME)
            else:
                oled.modal.DisplayVolume(oled.volume)
            emit_volume = True
        if oled.state == STATE_VOLUME:
            #SetState(STATE_VOLUME)
            if dir == RotaryEncoder.LEFT:
                oled.volume -= VOLUME_DT
                oled.volume = max(oled.volume, 0)
                #oled.modal.DisplayVolume(oled.volume)
            elif dir == RotaryEncoder.RIGHT:
                oled.volume += VOLUME_DT
                oled.volume = min(oled.volume, 100)
                #oled.modal.DisplayVolume(oled.volume)
            oled.stateTimeout = 2.0
            oled.modal.DisplayVolume(oled.volume)


def RightKnob_PushEvent(hold_time):
    global UPDATE_INTERVAL
    if hold_time < 1:
        print ('LeftKnob_PushEvent SHORT')
        if oled.state == STATE_PLAYER:
            if oled.playState == 'play':
                volumioIO.emit('stop')
            else:
                volumioIO.emit('play')
        if oled.state == STATE_QUEUE_MENU:
            print ('RightKnob_PushEvent SHORT')
            oled.stateTimeout = 0

    else:
        print ('LeftKnob_PushEvent LONG -> trying to shutdown')
        UPDATE_INTERVAL = 10 #stop updating screen
        sleep(0.1)
        show_logo("shutdown.ppm", oled)
        try:
            with open('oledconfig.json', 'w') as f:   #save current track number
                json.dump({"track": oled.playPosition}, f)
        except IOError:
            print ('Cannot save config file to current working directory')
        sleep(1.5)
        oled.cleanup()            # put display into low power mode
        volumioIO.emit('shutdown')
        sleep(60)

def LeftKnob_RotaryEvent(dir):
    global emit_track
    oled.stateTimeout = 6.0
    if oled.state == STATE_PLAYER:
        SetState(STATE_QUEUE_MENU)
    elif oled.state == STATE_QUEUE_MENU and dir == RotaryEncoder.LEFT:
        oled.modal.PrevOption()
        oled.selQueue = oled.modal.SelectedOption()
        emit_track = True
    elif oled.state == STATE_QUEUE_MENU and dir == RotaryEncoder.RIGHT:
        oled.modal.NextOption()
        oled.selQueue = oled.modal.SelectedOption()
        emit_track = True

def LeftKnob_PushEvent(hold_time):
    if hold_time < 1:
        if oled.state == STATE_PLAYER:
            SetState(STATE_QUEUE_MENU)
        if oled.state == STATE_QUEUE_MENU:
            print ('RightKnob_PushEvent SHORT')
            oled.stateTimeout = 0

#________________________________________________________________________________________
#________________________________________________________________________________________
#    
#    ____        __  __                  _       __      __       __                  
#   / __ )__  __/ /_/ /_____  ____      | |     / /___ _/ /______/ /_  ___  _____   _ 
#  / __  / / / / __/ __/ __ \/ __ \_____| | /| / / __ `/ __/ ___/ __ \/ _ \/ ___/  (_)
# / /_/ / /_/ / /_/ /_/ /_/ / / / /_____/ |/ |/ / /_/ / /_/ /__/ / / /  __/ /     _   
#/_____/\__,_/\__/\__/\____/_/ /_/      |__/|__/\__,_/\__/\___/_/ /_/\___/_/     (_)  
#   
ButtonA_Push = PushButton(oledBtnA, max_time=2)
ButtonA_Push.setCallback(ButtonA_PushEvent)
ButtonB_Push = PushButton(oledBtnB, max_time=2)
ButtonB_Push.setCallback(ButtonB_PushEvent)
ButtonC_Push = PushButton(oledBtnC, max_time=2)
ButtonC_Push.setCallback(ButtonC_PushEvent)
ButtonD_Push = PushButton(oledBtnD, max_time=2)
ButtonD_Push.setCallback(ButtonD_PushEvent)

LeftKnob_Push = PushButton(oledLtrBtn, max_time=2)
LeftKnob_Push.setCallback(LeftKnob_PushEvent)
LeftKnob_Rotation = RotaryEncoder(oledLtrLeft, oledLtrRight, pulses_per_cycle=4)
LeftKnob_Rotation.setCallback(LeftKnob_RotaryEvent)

RightKnob_Push = PushButton(oledRtrBtn, max_time=2)
RightKnob_Push.setCallback(RightKnob_PushEvent)
RightKnob_Rotation = RotaryEncoder(oledRtrLeft, oledRtrRight, pulses_per_cycle=4)
RightKnob_Rotation.setCallback(RightKnob_RotaryEvent)
#________________________________________________________________________________________
#________________________________________________________________________________________
#    
#    ____              __        __                          
#   / __ )____  ____  / /_      / /   ____  ____ _____     _ 
#  / __  / __ \/ __ \/ __/_____/ /   / __ \/ __ `/ __ \   (_)
# / /_/ / /_/ / /_/ / /_/_____/ /___/ /_/ / /_/ / /_/ /  _   
#/_____/\____/\____/\__/     /_____/\____/\__, /\____/  (_)  
#    
show_logo(oledBootLogo, oled)
sleep(2)
SetState(STATE_PLAYER)
#________________________________________________________________________________________
#________________________________________________________________________________________
#  
#   __  __          __      __          ________                        __         
#  / / / /___  ____/ /___ _/ /____     /_  __/ /_  ________  ____ _____/ /____   _ 
# / / / / __ \/ __  / __ `/ __/ _ \     / / / __ \/ ___/ _ \/ __ `/ __  / ___/  (_)
#/ /_/ / /_/ / /_/ / /_/ / /_/  __/    / / / / / / /  /  __/ /_/ / /_/ (__  )  _   
#\____/ .___/\__,_/\__,_/\__/\___/    /_/ /_/ /_/_/   \___/\__,_/\__,_/____/  (_)  
#    /_/ 
#     
updateThread = Thread(target=display_update_service)
updateThread.daemon = True
updateThread.start()

def _receive_thread():
    volumioIO.wait()

receive_thread = Thread(target=_receive_thread)
receive_thread.daemon = True
receive_thread.start()

volumioIO.on('pushState', onPushState)
volumioIO.on('pushQueue', onPushQueue)

# get list of Playlists and initial state
volumioIO.emit('listPlaylist')
volumioIO.emit('getState')
volumioIO.emit('getQueue')

sleep(0.1)

try:
    with open('oledConfigurationFiles.json', 'r') as f:   #load last playing track number
        config = json.load(f)
except IOError:
    pass
else:
    oled.playPosition = config['track']
    
InfoTag = 0                         #helper for missing Artist/Song when changing sources
GetIP()

def PlaypositionHelper():
    while True:
          volumioIO.emit('getState')
          sleep(1.0)
PlayPosHelp = threading.Thread(target=PlaypositionHelper, daemon=True)
PlayPosHelp.start()
#________________________________________________________________________________________
#________________________________________________________________________________________
#	
#    __  ___      _             __                          
#   /  |/  /___ _(_)___        / /   ____  ____  ____     _ 
#  / /|_/ / __ `/ / __ \______/ /   / __ \/ __ \/ __ \   (_)
# / /  / / /_/ / / / / /_____/ /___/ /_/ / /_/ / /_/ /  _   
#/_/  /_/\__,_/_/_/ /_/     /_____/\____/\____/ .___/  (_)  
#  
while True:
#    print('State: ', oled.state)
#    print('palyState: ', oled.playState)
#    print('newStatus: ', newStatus)
#    print(oled.modal)
    if emit_volume:
        emit_volume = False
        print("volume: " + str(oled.volume))
        volumioIO.emit('volume', oled.volume)
    if emit_track and oled.stateTimeout < 4.5:
        emit_track = False
        try:
            SetState(STATE_PLAYER)
            InfoTag = 0
        except IndexError:
            pass
        volumioIO.emit('stop')
        sleep(0.01)
        volumioIO.emit('play', {'value':oled.selQueue})
    sleep(0.1)

#this is the loop to push the actual time every 0.1sec to the "Standby-Screen"
    if oled.state == STATE_PLAYER and newStatus == 'stop' and oled.ShutdownFlag == False:
        InfoTag = 0  #resets the InfoTag helper from artist/song update loop
        oled.state = 0
        oled.time = strftime("%H:%M:%S")
        SetState(STATE_PLAYER)
        oled.modal.UpdateStandbyInfo()
        sleep(0.2)  

#if playback is paused, here is defined when the Player goes back to "Standby"/Stop		
    if oled.state == STATE_PLAYER and newStatus == 'pause' and varcanc == True:
        secvar = int(round(time()))
        varcanc = False
    elif oled.state == STATE_PLAYER and newStatus == 'pause' and int(round(time())) - secvar > oledPause2StopTime:
        varcanc = True
        volumioIO.emit('stop')
        oled.modal.UpdateStandbyInfo()
        secvar = 0.0

    if oled.state == STATE_PLAYER and newStatus == 'play' and oled.ScreenTimerStart == True:
        oled.ScreenTimerStamp = int(round(time()))
        oled.ScreenTimerStart = False
        oled.ScreenTimer10 = True

    if oled.state == STATE_PLAYER and newStatus != 'stop': 
        if oled.ScreenTimer10 == True and (int(round(time())) - oled.ScreenTimerStamp > oled.ScreenTimerChangeTime):
            oled.ScreenTimerChangeTime
            oled.ScreenTimer10 = False
            oled.ScreenTimer20 = True
        if oled.ScreenTimer20 == True and ((int(round(time())) - oled.ScreenTimerStamp) > (oled.ScreenTimerChangeTime * 2)):
            oled.ScreenTimer20 = False
            oled.ScreenTimerStart = True
            oled.ScreenTimerStamp = 0.0
            oled.ScreenTimer10 = True
    
    if oled.state != STATE_PLAYER:
        oled.ScreenTimer10 = False
        oled.ScreenTimer20 = False
        oled.ScreenTimerStart = True
        oled.ScreenTimerStamp = 0.0
    #print('oled.ScreenTimer10: ', oled.ScreenTimer10)
    #print('oled.ScreenTimer20 :', oled.ScreenTimer20)
    #print('oled.ScreenTimerStart :', oled.ScreenTimerStart)
    #print('oled.ScreenTimerStamp :', oled.ScreenTimerStamp)
    #print('oled.stateTimeout: ', oled.stateTimeout)
    #print('oled.timeOutRunning: ', oled.timeOutRunning)
    #print('oled.state: ', oled.state)
    #print('newStatus: ', newStatus)
    #print('oled.playState: ', oled.playState)

sleep(0.02)
