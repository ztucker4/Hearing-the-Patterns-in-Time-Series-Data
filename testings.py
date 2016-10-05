from stockPredictor import *

if __name__ == '__main__':
    pricesData = readStock('wiki-goog.csv')
    dateData = getDates('wiki-goog.csv')
    for i in range(len(dateData)):
        dateData[i] = datetime.strptime(dateData[i], '%Y-%m-%d')
    days=mdates.DayLocator()
    daysFmt=mdates.DateFormatter('%m/%d')
    fig,ax = plt.subplots()
    ax.xaxis.set_major_formatter(daysFmt)
    ax.xaxis.set_major_locator(days)
    ax.plot(dateData[63:70],pricesData[63:70])
    ax.plot(dateData[66:68],pricesData[66:68],'r-',linewidth = 2.0)
    start, end = ax.get_xlim()
    #ax.xaxis.set_ticks(np.arange(start, end, stepsize))
    plt.show()
