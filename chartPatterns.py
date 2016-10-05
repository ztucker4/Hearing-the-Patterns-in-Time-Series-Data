from stockPredictor import *
import matplotlib.pyplot as plt
import glob

def getMinMax(pricesList):
    """takes a list of stock prices and returns a list of indices of the
        mins/maxes and a list of labels corresponding to these indices"""
    indicesList = []
    labelsList = []
    for i in range(1,len(pricesList)-1):
        #if the surrounding points are lower, it's a max
        if (pricesList[i-1]<pricesList[i] and pricesList[i+1]<pricesList[i]):
            indicesList.append(i)
            labelsList.append('max')
        #if the surrounding points are higher, it's a min
        elif (pricesList[i-1]>pricesList[i] and pricesList[i+1]>pricesList[i]):
            indicesList.append(i)
            labelsList.append('min')
    return indicesList,labelsList

def isHS(indicesList,labelsList,pricesList):
    """checks if the given subset of a stock matches the head and shoulders
    pattern"""
    if labelsList == ['max','min','max','min','max']:
        if pricesList[indicesList[0]] <pricesList[indicesList[2]] and\
           pricesList[indicesList[2]] > pricesList[indicesList[4]] and\
           pricesList[indicesList[0]] - pricesList[indicesList[4]]<3:
            return True
    return False


def lookForHS(stockName):
    """looks for head and shoulders patterns in a given stock"""
    #read in the stock data and find the local mins and maxes
    pricesList = readStock('WIKI-' +stockName +'.csv')
    indicesList,labelsList = getMinMax(pricesList)

    #locationsBools is True at i if i (in indicesList)
    #begins a head and shoulders pattern in the original data
    locationsBools= []
    for i in range(len(indicesList)-6):
        locationsBools.append(isHS(indicesList[i:i+5], labelsList[i:i+5],
                                pricesList))
    #extract the locations where it is true
    trues = [i for i, x in enumerate(locationsBools) if x]

    #now find these indices in the original dataset
    finalIndicesList = []
    for i in range(len(trues)):
        finalIndicesList.append(indicesList[trues[i]])

    #plot each located pattern
    j = 0
    while j <len(finalIndicesList):
        drawHS(j,indicesList,finalIndicesList,trues,pricesList)
        plt.waitforbuttonpress()
        plt.close()
        j = j +1

def drawHS(j,indicesList,finalIndicesList,trues,pricesList):
    """helper function to draw the graphs of the head and shoulders patterns"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    patternLength = indicesList[trues[j] + 6] - indicesList[trues[j]]
    #plot the head and shoulders
    ax.plot(range(finalIndicesList[j]-1,finalIndicesList[j] + patternLength),
             pricesList[finalIndicesList[j]-1:finalIndicesList[j]+\
                        patternLength],linewidth = 3.0)
    #put dots on the head and shoulders
    ax.plot([indicesList[trues[j]],indicesList[trues[j]+2],
             indicesList[trues[j]+4]],[pricesList[indicesList[trues[j]]],
             pricesList[indicesList[trues[j]+2]],
             pricesList[indicesList[trues[j] +4]]],'ro')
    #draw the neckline
    ax.plot([indicesList[trues[j]+1],indicesList[trues[j]+3]],
             [pricesList[indicesList[trues[j]+1]],
             pricesList[indicesList[trues[j]+3]]],'g-')
    plt.draw()

def findTrendLine(stockName,startIndex,numOfLines):
    """finds and plots the trendlines for the stock starting at the
        given index, numOfPlots times"""
    #read in stock and start in the correct place
    pricesList = readStock('WIKI-' +stockName +'.csv')
    pricesList = pricesList[startIndex:]
    finalList = []
    for k in range(numOfLines+1):
        #find the mins and maxes
        #we do this every time 
        indicesList,labelsList = getMinMax(pricesList)
        indicesList = indicesList[k:]
        labelsList = labelsList[k:]
        
        #find the first, second, and third min and max
        #we'll use the first two to make the trend lines
        firstMin = indicesList[labelsList.index('min')]
        firstMax= indicesList[labelsList.index('max')]
        secondMin = indicesList[labelsList.index('min') +2]
        secondMax = indicesList[labelsList.index('max') +2]
        thirdMin = indicesList[labelsList.index('min') +4]
        thirdMax = indicesList[labelsList.index('max') +4]

        #combine the data into lists for access later
        minY = [pricesList[firstMin],pricesList[secondMin]]
        minX = [firstMin,secondMin]
        maxY = [pricesList[firstMax], pricesList[secondMax]]
        maxX = [firstMax,secondMax]

        #compute the slope and y-intercept given by the mins and maxes
        minSlope = (minY[0]-minY[1])/(minX[0]-minX[1])
        maxSlope = (maxY[0]-maxY[1])/(maxX[0]-maxX[1])
        minIntercept = minY[0] -minSlope*minX[0]
        maxIntercept = maxY[0] -maxSlope*maxX[0]

        #add the third min and max in so we extend the trend lines far enough
        minX.append(thirdMin)
        maxX.append(thirdMax)

        #create some data points along the min and max trend lines
        #so we can plot them along with the data
        maxLine = []
        for i in maxX:
            maxLine.append(maxSlope*i + maxIntercept)
        minLine = []    
        for i in minX:
            minLine.append(minSlope*i + minIntercept)

        paramsList = [pricesList,firstMin,secondMin,thirdMin,firstMax,secondMax,
                    thirdMax,minLine,maxLine]
        finalList.append(paramsList)
    graphTrends(finalList)

def graphTrends(finalList):
    """helper function to plot the trendlines and the original data"""
    
    for i in range(len(finalList)):
        #get the parameters out of the list
        pricesList = finalList[i][0]
        firstMin = finalList[i][1]
        secondMin = finalList[i][2]
        thirdMin = finalList[i][3]
        firstMax = finalList[i][4]
        secondMax = finalList[i][5]
        thirdMax = finalList[i][6]
        minLine = finalList[i][7]
        maxLine = finalList[i][8]

        #now we can plot the data
        #offset everything by i!
        plt.plot(range(min(firstMin,firstMax)+i,max(thirdMin,thirdMax)+i),
                 pricesList[min(firstMin,firstMax)+i:max(thirdMin,thirdMax)+i],
                 'b-',linewidth=2.0)
        #plot minima lines in red, maxima lines in green
        plt.plot([firstMin,secondMin,thirdMin],minLine,'r-')
        plt.plot([firstMax,secondMax,thirdMax],maxLine,'g-')
    plt.show()

    
def main():
    mode = raw_input('''Enter 'HS' to look for head and shoulders patterns
in a stock, or enter 'trends' to find the trend lines for a stock: ''')
    
    #look for head and shoulders
    if mode.lower() == 'hs':
        possibleFiles = glob.glob('*.csv')
        for i in range(len(possibleFiles)):
            possibleFiles[i] = possibleFiles[i][5:-4]
        print 'Currently available stocks: ' + str(possibleFiles)
        stockName = raw_input('Enter the name of the desired stock (e.g. \
GOOG, AAPL): ')
        lookForHS(stockName)

    #look for trendlines
    elif mode.lower() == 'trend' or mode.lower() == 'trends':
        possibleFiles = glob.glob('*.csv')
        for i in range(len(possibleFiles)):
            possibleFiles[i] = possibleFiles[i][5:-4]
        print 'Currently available stocks: ' + str(possibleFiles)
        stockName = raw_input('Enter the name of the desired stock (e.g. \
GOOG, AAPL): ')
        startIndex = input('Enter the numerical index of the date you \
wish to start on: ')
        numOfLines = input('Enter the number of trends lines you \
wish to see: ')                               
        findTrendLine(stockName,startIndex,numOfLines)
        
        
    
        

if __name__== '__main__':
    main()
    


