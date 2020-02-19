"""
Overview: Simulate the electrolitic tank experiment for a known set of boundry
conditions.
Author: BenGfoyle - github.com/bengfoyle
"""


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#===============================================================================
def makePlot(x,y):
    """
    Oberview: Make a plot of one parameter vs another
    """
    plt.scatter(x,y)
    plt.show()
#===============================================================================

#===============================================================================
def makeGrid(row,col):
    """
    Overview: Define a grid for the experiment, with some given boundry codition
    """
    grid = np.full((row, col), 0.0)
    for i in range(0,len(grid)):
        if i == 0 or i == len(grid) - 1:
            for j in range(0,len(grid[i])):
                if j >= col/2:
                    grid[i][j] = 100.0
        grid[i][len(grid[i]) - 1] = 100.0
    return grid
#===============================================================================

#===============================================================================
def sumAround(i,j,grid):
    """
    Overview: Sum values around a point, and returns average.
    """


    # To impliment a 8 point meausrment use the following:
    # newValue = grid[i + 1][j] + grid[i - 1][j] + \
    # grid[i + 1][j - 1] + grid[i - 1][j - 1] + grid[i][j - 1] + \
    # grid[i + 1][j + 1] + grid[i - 1][j + 1] + grid[i][j + 1]
    # avg = newValue / 8


    newValue = grid[i + 1][j] + grid[i - 1][j] + grid[i][j + 1] + grid[i][j - 1]
    avg = round(newValue / 4,2)
    return avg
#===============================================================================

#===============================================================================
def iterateElectrode(row,col,grid,iterations):
    """
    Overview: Iterate over the relative parts of the grid
    """
    n = 0
    while n < iterations:
        for i in range(1,row - 1):
            for j in range(1, col -1):
                grid[i][j] = sumAround(i,j,grid)
        n += 1
    return grid
#===============================================================================

#===============================================================================
def calX(ix, row, p,rightElectrode):
    """
    Overview: Calulate the xVal associated a given row, index and percentile.
    """
    distance = 1
    v1 = abs(row[ix] - row[ix + 1])
    v2 = abs(row[ix] - row[ix - 1])
    if v2 > v1:
        v = v1
    else:
        v = v2

    if v > row[ix]:
        vH = v; vL = row[ix]
    else:
        vL = v; vH = row[ix]

    if rightElectrode == True:
        ix += 1
        distance += 1

    if int(vH) == int(vL):
        return ix
    else:
        return ix + (((p - vL)/(vH - vL)) * distance)
#===============================================================================

#===============================================================================
def findNearest(row, target):
    """
    Overview: Return the index of the element closest to value
    """
    return min(enumerate(row), key=lambda x: abs(target - x[1]))[0]
#===============================================================================

#===============================================================================
def getXVals(grid,percentiles):
    """
    Overview: Return the corresponding xVals for each percentile
    """
    xVals = []
    print(len(grid))
    for i in range(0,len(grid)):
        print(i)
        for p in percentiles:
            near = findNearest(grid[i],p)
            rightElectrode = False
            try:
                if i == len(grid)/2:
                    rightElectrode = True
                xVals.append(calX(near,grid[i],p,rightElectrode))
            except:
                pass
        xVals.append("*")

    return xVals
#===============================================================================
row = 11; col = 24; iterations = 150
percentiles = [10,20,30,40,50,60,70,80,90]
grid = makeGrid(row,col)
iterGrid = iterateElectrode(row,col,grid,iterations)
xVals = getXVals(grid,percentiles)
data = pd.DataFrame(xVals)
data.to_csv("xVals.csv")
data = pd.DataFrame(iterGrid)
data.to_csv("simulationOutput.csv")

ax = sns.heatmap(grid,linewidth = 0.5)

plt.show()
