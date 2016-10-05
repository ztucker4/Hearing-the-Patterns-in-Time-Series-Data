from math import *
from bisect import bisect_left
import collections
import csv
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def getUD(angle):
    """helper function to determine if given angle is up or down"""
    if angle > 0:
        return 'up'
    elif angle < 0:
        return 'down'
    else:
        return 'none'

def getUDS(angle):
    """helper function to determine if given angle is up, down, or same"""
    if angle < -pi/6:
        return 'down'
    elif angle > pi/6:
        return 'up'
    else:
        return 'same'

def readStock(filename):
    """given file name as a string, return a list of the opening prices.
        assumes that these are in the second column (like from quandl)"""
    data = csv.reader(open(filename, 'rb'))
    column = []
    for row in data:
        column.append(row[1])
    column = column[1:]
    #remove empty entries
    newColumn = []
    for i in range(len(column)):
        if column[i] != '':
            newColumn.append(float(column[i]))
    return newColumn

def getDates(filename):
    """given file name as a string, return a list of the associated dates.
        assumes that these are in the firsts column (like from quandl)"""
    data = csv.reader(open(filename, 'rb'))
    column = []
    for row in data:
        column.append(row[0])
    column = column[1:]
    return column

def makeStockList(stockData,divNum,stopIndex):
    """converts the stock prices into a list of angles approximately matching
    the stock data. divNum is the number of possible angles, stopIndex is
    the index of the last desired endpoint"""
    perSlice = pi/(divNum-1)
    possibleAngles = [-pi/2]
    finalList = []
    stockAngles = getAngles(stockData)
    for i in range(divNum-1):
        possibleAngles.append(possibleAngles[i]+perSlice)
    for i in range(stopIndex+1):
        finalList.append(findClosest(possibleAngles,stockAngles[i]))
    return finalList

def getAngles(stockList):
    """given a list of stock prices,
        find the angle at each point. helper function for makeStockList."""
    angles= []
    for i in range(len(stockList)-1):
        currentSlope = stockList[i+1]-stockList[i]
        currentAngle = atan2(currentSlope,1)
        angles.append(currentAngle)
    angles.append(float('inf'))
    return angles    

def findClosest(anglesList,angle):
    """find the angle closest to the given angle of the angles given in the
    (sorted) list. ties resolve down."""
    ind = bisect_left(anglesList,angle)
    if ind == 0:
        return anglesList[0]
    if ind == len(anglesList):
        return anglesList[-1]
    before = anglesList[ind - 1]
    after = anglesList[ind]
    if after - angle < angle - before:
       return after
    else:
       return before
    
def makeMarkovDict(stockList, k):
    """makes a markov dictionary based on the given data and desired order.
    i.e. write out the possibilities for the next piece of data, given the
    length-k sublist preceding it."""
    dictionary = {}
    for i in range(len(stockList)-k):
        #put current substring into a tuple
        currentEntry = ()
        for j in range(k):
            currentEntry = currentEntry + (stockList[i+j],)
        #if the entry hasn't been seen before, add it
        if currentEntry not in dictionary:
            dictionary[currentEntry] = [stockList[i+j+1]]
        #otherwise, append our new possibility
        else:
            dictionary[currentEntry].append(stockList[i+j+1])
    return dictionary

def makeMarkovDictEfficient(stockList,targetList):
    """makes the dictionary entry only for the desired sublist."""
    dictionary = {}
    k = len(targetList)
    targetTuple = tuple(targetList)
    for i in range(len(stockList)-k-1):
        if stockList[i:i+k] == targetList:
            if targetTuple not in dictionary:
                dictionary[targetTuple] = [stockList[i+k+1]]
            else:
                dictionary[targetTuple].append(stockList[i+k+1])
    return dictionary

def analyzeDict(markovDict):
    """returns a dict containing a counter value for each key, counting
    the frequency of each value for the corresponding key in the input dict"""
    countersList = []
    countersDict = {}
    for i in range(len(markovDict.keys())):
        countersList.append(
            collections.Counter(markovDict[markovDict.keys()[i]]))
    for i in range(len(markovDict)):
        countersDict[markovDict.keys()[i]] = countersList[i]
    return countersDict

def findNextAngle(stockAnglesList,countersDict,k):
    """look at the end of the given list and use the countersDict to predict
    the next angle"""
    currentKey = tuple(stockAnglesList[-k:])
    possible = countersDict[currentKey]
    bestAngle = possible.most_common(1)
    return bestAngle[0][0]

def lookForCloseWindows(targetTuple,countersDict):
    """finds windows at most 1 different from target"""
    possibleKeys = []
    totalCounter = collections.Counter()
    for key in countersDict:
        for i in range(len(targetTuple)):
            if key[:i] == targetTuple[:i] and key[i+1:] == targetTuple[i+1:]:
                possibleKeys.append(key)
    for key in possibleKeys:
        totalCounter = totalCounter + countersDict[key]
    return totalCounter

def standardAlgorithm():
    """runs the standard Markov chain algorithm"""
    #find available files and display them
    possibleFiles = glob.glob('*.csv')
    for i in range(len(possibleFiles)):
        possibleFiles[i] = possibleFiles[i][5:-4]
    print 'Currently available stocks: ' + str(possibleFiles)
    
    #get parameters from user
    stockName = raw_input('Enter the name of the stock (e.g. GOOG, KO): ')
    divNum = input('Enter the number of angles to divide the semicircle: ')
    k = input('Enter the order of the desired Markov model: ')
    startDate = raw_input('Enter the day you want to predict (YYYY-MM-DD): ')
    
    #read in data and check if parameters are valid
    filename = 'WIKI-' + stockName + '.csv'
    stockData = readStock(filename)
    dateData = getDates(filename)
    if startDate in dateData:
        stopIndex = dateData.index(startDate) -1
    else:
        print('The given date is not a valid trading day.')
        answer = raw_input('Try again? y/n ')
        return answer
    
    #use markov functions to predict next angle
    stockAnglesList = makeStockList(stockData, divNum,stopIndex)
    markovDict = makeMarkovDictEfficient(stockAnglesList,stockAnglesList[-k:])
    countersDict = analyzeDict(markovDict)
    nextAngle = findNextAngle(stockAnglesList,countersDict,k)
    
    #compute the relative frequency of our prediction
    currentKey = tuple(stockAnglesList[-k:])
    totalNum = sum(countersDict[currentKey].values())
    percent = 100.0*(countersDict[currentKey].most_common()[0][1])/totalNum

    print
    print 'The current angles are '+ str(stockAnglesList[-k:])
    print 'This pattern happened ' + str(totalNum) + ' times'
    print 'The next angle will probably be ' + str(nextAngle)
    print 'This happened ' + str(percent) +'% of the time'

    #if we can, check if our prediction is correct
    if dateData[-1] > startDate:
        actualAngle = getAngles(stockData)[stopIndex]
        print 'The actual angle was ' +str(actualAngle)
    if getUDS(actualAngle) == getUDS(nextAngle):
        print 'We were correct (up to up, down, or same)!'
    else:
        print 'We were wrong (up to up, down, or same) :('
    graphStock(stockData,dateData,stopIndex,k,nextAngle)
    answer = raw_input('Try again? y/n ')
    return answer

def fuzzyAlgorithm():
    """runs the fuzzy Markov algorithm"""
    #find available files and display them
    possibleFiles = glob.glob('*.csv')
    for i in range(len(possibleFiles)):
        possibleFiles[i] = possibleFiles[i][5:-4]
    print 'Currently available stocks: ' + str(possibleFiles)

    #get parameters from user
    stockName = raw_input('Enter the name of the stock (e.g. GOOG, KO): ')
    divNum = input('Enter the number of angles to divide the semicircle: ')
    k = input('Enter the order of the desired Markov model (k): ')
    startDate = raw_input("""Enter the day you want to predict (YYYY-MM-DD):""")
    
    #read in data and check if parameters are valid
    filename = 'WIKI-' + stockName + '.csv'
    stockData = readStock(filename)
    dateData = getDates(filename)
    if startDate in dateData:
        stopIndex = dateData.index(startDate) - 1
    else:
        print('the given date is not a valid trading day.')
        answer = raw_input('Try again? y/n ')
        return answer

    #use fuzzy markov functions to predict next angle
    stockAnglesList = makeStockList(stockData, divNum,stopIndex)
    #can't use efficient Markov Dict - we need the whole thing
    markovDict = makeMarkovDict(stockAnglesList,k) 
    countersDict = analyzeDict(markovDict)

    #compute the relative frequency of our prediction    
    currentKey = tuple(stockAnglesList[-k:])
    closeCounter = lookForCloseWindows(currentKey,countersDict)
    nextAngle = closeCounter.most_common(1)[0][0]
    totalNum = sum(closeCounter.values())
    percent = 100.0*(closeCounter.most_common(1)[0][1])/totalNum

    print
    print 'The current angles are '+ str(stockAnglesList[-k:])
    print 'This pattern happened (within one difference) ' +\
          str(totalNum) + ' times'
    print 'The next angle will probably be ' + str(nextAngle)
    print 'This happened ' + str(percent) +'% of the time'
    if dateData[-1] > startDate:
        actualAngle = getAngles(stockData)[stopIndex]
        print 'The actual angle was ' +str(actualAngle)
        if getUDS(actualAngle) == getUDS(nextAngle):
            print 'We were correct (up to up, down, or same)!'
        else:
            print 'We were wrong (up to up, down, or same) :('
    
    graphStock(stockData,dateData,stopIndex,k,nextAngle)
    answer = raw_input('Try again? y/n ')
    return answer

def graphStock(priceData,dateData,stopIndex,k,prediction):
    '''graphs the current stock and the predicted next angle'''
    #get the dates and prices we want to plot
    currentWindow = priceData[stopIndex-(k-1):stopIndex+3]
    currentDates = dateData[stopIndex-(k-1):stopIndex+3]
    
    #compute the next price
    priceDiff = tan(prediction)
    #if we predicted the next angle as pi/2 or -pi/2, the tan will be huge
    #we bring it back down to 12 to make the graph look reasonable
    if priceDiff >12:
        priceDiff = 12
    elif priceDiff < -12:
        priceDiff = -12
    nextPrice = currentWindow[-2] + priceDiff

    #convert the YYYY-MM-DD strings to datetime objects
    for i in range(len(currentDates)):
        currentDates[i] = datetime.strptime(currentDates[i], '%Y-%m-%d')

    #setting up the x axis parameters
    days = mdates.DayLocator()
    daysFmt = mdates.DateFormatter('%Y-%m-%d')

    #plot everything!
    fig,ax = plt.subplots()
    ax.plot(currentDates,currentWindow)
    ax.plot(currentDates[-2:],[currentWindow[-2],nextPrice],'r-')
    ax.plot(currentDates[0:k+1],currentWindow[0:k+1],'go')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)

    plt.show()


if __name__ == '__main__':
    while True:
        answer = 'n'
        alg = raw_input("""Enter 'standard' to use the standard Markov 
algorithm, or 'fuzzy' to use the fuzzy algorithm: """)
        print
        if alg == 'standard' or alg == 'Standard' or alg =='STANDARD':
            answer = standardAlgorithm()
        elif alg == 'fuzzy' or alg == 'Fuzzy' or alg == 'FUZZY':
            answer = fuzzyAlgorithm()
        if answer != 'y' and answer != 'Y':
            break
        print
        print
