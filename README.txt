README
------

This folder contains three python files (chartPatterns.py, stockPredictor.py, and stocksToAudio.py) as well as a few .csv files containing stock market data.
To run these programs, you will need Python 2.7, with the following packages installed:
glob, math, bisect, collections, csv, datetime, StringIO, pygame, music21, matplotlib
Of these, only the last three are not included with a standard installation of python. They can all be installed using pip.


chartPatterns.py
----------------
This file contains a collection of functions related to the identification of chart patterns in stock market data. Upon running the program, you will be prompted to choose whether to look for head and shoulders patterns in a stock, or to find trend lines in a stock. Enter 'hs' to enter Head and Shoulders mode, or 'trends' to enter Trendline mode.
The 'HS' selection will ask you for the name of a stock and then present you with a series of graphs showing places in the stock's history that resemble a head and shoulders pattern. The tops of the head and shoulders are indicated with red dots. Click anywhere on the figure to advance to the next located pattern. The y-axis of the graph shows the stock's price at the time, and the x-axis shows the index of the date in the given stock data file.
The 'trends' selection will prompt you for the name of a stock, the index of the day you wish to start at, and the number of different trend lines that will be plotted. The stock will then be plotted in blue, with trend lines connecting local minima plotted in red and lines connecting local maxima in green.


stockPredictor.py
-----------------
This file contains functions related to using a Markov chain model to predict the stock market. When running the program, you will be prompted to select either a 'standard' or 'fuzzy' version of the algorithm. You will then be presented with a choice of stocks and asked for some parameters for the model. Simply input the name of your desired stock, as well as the number of angles, the order for the Markov model (k), and your chosen date to predict. The program will then print its prediction, as well as information about how it was determined and whether it was correct. A graph will also appear showing the previous k days and the prediction. The actual prices for the stock are plotted in blue (with green dots highlighting the different days), and the prediction is plotted in red.


stocksToAudio.py
----------------
This program converts stock data into audio data, using a map between notes and angles. You will be prompted for the names of two stocks and a range of dates to convert to audio data. The program will then play an audio version of the stock data and show an animated graph that plots the angles corresponding to the notes in real time.