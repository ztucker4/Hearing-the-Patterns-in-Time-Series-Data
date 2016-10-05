from stockPredictor import *
from math import *
from music21 import *
import pygame
import StringIO
import glob
import matplotlib.pyplot as plt


#set up audio data
freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.set_volume(0.8)


def makeDiatonicPitches(thetaList):
    '''turns thetas into notes based on closest angle'''
    angleList = [-pi/2, -pi/3, -pi/6, 0, pi/6, pi/3, pi/2]
    pitchList = []
    for i in range(len(thetaList)):
        pitchList.append(findClosest(angleList,thetaList[i]))
    for j in range(len(pitchList)):
        if pitchList[j] in angleList:
            pitchList[j] = angleList.index(pitchList[j])
    return pitchList

    
def convertToStreamDiatonic(noteList):
    '''makes list of notes into music21 stream'''
    #lower notes are lower in the circle
    stream1 = stream.Stream()
    for i in range(len(noteList)):
        if noteList[i] == 0:
            name = "C4"
        elif noteList[i] ==1:
            name = "D4"
        elif noteList[i] == 2:
            name = "E4"
        elif noteList[i] == 3:
            name = "F4"
        elif noteList[i] == 4:
            name = "G4"
        elif noteList[i] == 5:
            name = "A4"
        elif noteList[i] == 6:
            name = "B4"
                
        notei = note.Note(name)
        stream1.append(notei)
    return stream1





if __name__ == "__main__":
    #find available files and display them
    possibleFiles = glob.glob('*.csv')
    for i in range(len(possibleFiles)):
        possibleFiles[i] = possibleFiles[i][5:-4]
    print 'Currently available stocks: ' + str(possibleFiles)
    
    stock1 = raw_input('Enter the name of the first stock (e.g. GOOG, FB): ')
    stock2 = raw_input('Enter the name of the second stock: ')
    startDate = raw_input('Enter the date to start listening (YYYY-MM-DD): ')
    stopDate = raw_input('Enter the date to stop listening (YYYY-MM-DD): ')

    #find the start and stop indices
    filename1 = 'WIKI-' + stock1 + '.csv'
    filename2 = 'WIKI-' + stock2 + '.csv'
    dateData = getDates(filename1)
    validStart = False
    validStop = False
    while validStart == False:
        if startDate in dateData:
            startIndex = dateData.index(startDate)
            validStart = True
        else:
            print 'The start date is not a valid trading day.'
            startDate = raw_input('Enter a new start date: ')
    while validStop == False:
        if stopDate in dateData:
            stopIndex = dateData.index(stopDate)
            validStop = True
        else:
            print 'The stop date is not a valid trading day.'
            stopDate = raw_input('Enter a new stop date: ')
        
    
    #do everything for stock 1
    data1 = readStock(filename1)[startIndex:stopIndex]
    thetas1 = getAngles(data1)
    notes1 = makeDiatonicPitches(thetas1)
    stream1 = convertToStreamDiatonic(notes1)
    
    #now for stock 2
    data2 = readStock(filename2)[startIndex:stopIndex]
    thetas2 = getAngles(data2)
    notes2 = makeDiatonicPitches(thetas2)
    stream2 = convertToStreamDiatonic(notes2)
    
    #now put it all in a score and convert to midi
    totalScore = stream.Score()
    totalScore.insert(0,stream1)
    totalScore.insert(0,stream2)
    totalMidi = midi.translate.streamToMidiFile(totalScore)
    totalStr= totalMidi.writestr()
    totalFile = StringIO.StringIO(totalStr)
    
   
    #now start the pygame stuff
    pygame.init()
    #play the music!
    pygame.mixer.music.load(totalFile)
    pygame.mixer.music.play()
    
    #loop over the price data to plot it one note at a time
    for i in range(len(data1)):
        plt.plot(data1[:i],'b-')
        plt.plot(data2[:i],'r-')
        plt.draw()
        plt.pause(0.4)

    #and we're done!    
    plt.pause(1)
    plt.close()
    pygame.quit()
    
    
