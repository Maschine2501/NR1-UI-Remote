#!/usr/bin/python3

#___________________________________________________________________
#config for boot- and shutdown-logo
oledBootLogo = "volumio_logo.ppm"
oledShutdownLogo = "shutdown.ppm"

#___________________________________________________________________
#config for Clock/Standby:
oledtext03 = 0, 2       #clock
oledtext04 = 0, 118      #IP
oledtext05 = 40, 30     #Date
oledtext09 = 116, 118     #LibraryInfoIcon

#_______'No-Spectrum'-Screen1_____________________________________________________
#Config TextPositions NowPlaying-/StandBy-Screen:
Screen1text01 = 0, 2        #Artist
Screen1text09 = 0, 22         #Album
Screen1text02 = 0, 36       #Title
Screen1text06 = 0, 92       #format
Screen1text07 = 32, 92     #samplerate
Screen1text08 = 90, 92     #bitdepth
Screen1text28 = 46, 106       #Play/Pause Indicator

#configuration of the duration and playtime (textbox-) positions
Screen1ActualPlaytimeText = 0, 108
Screen1DurationText = 84, 108

#config for Progress-Bar
Screen1barwidth = 128
Screen1barLineBorder = (0, 255, 0)
Screen1barLineFill = 'black'
Screen1barLineX = 0
Screen1barLineThick1 = 124     #difference between both = thickness 
Screen1barLineThick2 = 125     # 59 and 59 = 1 Pixel thick
Screen1barBorder = (0, 255, 0)
Screen1barFill = (0, 255, 0)
Screen1barX = 0
Screen1barThick1 = 122         #difference between both = thickness 
Screen1barThick2 = 127         # 56 and 62 = 6 Pixel thick
Screen1barNibbleWidth = 3

#_______'No-Spectrum'-Screen2_____________________________________________________
#Config TextPositions NowPlaying-/StandBy-Screen:
Screen2text01 = 0, 2        #Artist
Screen2text02 = 0, 92       #Title
Screen2text06 = 0, 41       #format
Screen2text07 = 32, 41     #samplerate
Screen2text08 = 90, 41     #bitdepth
Screen2text28 = 46, 106       #Play/Pause Indicator

#configuration of the duration and playtime (textbox-) positions
Screen2ActualPlaytimeText = 0, 108
Screen2DurationText = 84, 108

#config for Progress-Bar
Screen2barwidth = 128
Screen2barLineBorder = (0, 255, 0)
Screen2barLineFill = 'black'
Screen2barLineX = 0
Screen2barLineThick1 = 124     #difference between both = thickness 
Screen2barLineThick2 = 125     # 59 and 59 = 1 Pixel thick
Screen2barBorder = (0, 255, 0)
Screen2barFill = (0, 255, 0)
Screen2barX = 0
Screen2barThick1 = 122         #difference between both = thickness 
Screen2barThick2 = 127         # 56 and 62 = 6 Pixel thick
Screen2barNibbleWidth = 3

#___________________________________________________________________
#Config TextPositions Media-Library-Info-Screen:
oledtext10 = 80, 2      #Number of Artists
oledtext11 = 80, 15     #Number of Albums
oledtext12 = 80, 28     #Number of Songs
oledtext13 = 80, 41     #Summary of duration
oledtext14 = 14, 2       #Text for Artists
oledtext15 = 14, 15      #Text for Albums
oledtext16 = 14, 28      #Text for Songs
oledtext17 = 14, 41      #Text for duration
oledtext18 = 60, 52     #Menu-Label Icon
oledtext19 = 120, 54     #LibraryInfoIcon
oledtext20 = 0, 2        #icon for Artists
oledtext21 = 0, 15       #icon for Albums
oledtext22 = 0, 28       #icon for Songs
oledtext23 = 0, 41       #icon for duration

#___________________________________________________________________
#configuration Menu-Screen:
oledListEntrys = 8
oledEmptyListText = 'no items..'
oledEmptyListTextPosition = 0, 4
oledListTextPosX = 0
oledListTextPosY = 16    #height of each Entry (4x16 = 64)

#___________________________________________________________________
#config for Text:
oledArt = 'Interpreten :'  #sets the Artists-text for the MediaLibrarayInfo
oledAlb = 'Alben :'        #sets the Albums-text for the MediaLibrarayInfo
oledSon = 'Songs :'        #sets the Songs-text for the MediaLibrarayInfo
oledPla = 'Playtime :'     #sets the Playtime-text for the MediaLibrarayInfo

#___________________________________________________________________
#config for Icons:
oledlibraryInfo = '\U0001F4D6'
oledlibraryReturn = '\u2302'
oledArtistIcon = '\uF0F3'
oledAlbumIcon = '\uF2BB'
oledSongIcon = '\U0000F001'
oledPlaytimeIcon = '\U0000F1DA'
oledplayIcon = '\u25B6'
oledpauseIcon = '\u2389'

#____________________________________________________________________
#config for Scrolling Text
ArtistScrollSpeed = 1
ArtistEndScrollMargin = 2
SongScrollSpeed = 1
SongEndScrollMargin = 2
AlbumScrollSpeed = 1
AlbumEndScrollMargin = 2
