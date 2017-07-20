# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 15:32:04 2017

@author: skyhiter
"""

import numpy as np

FILENAME = 'R101.txt'
ROW = 26
STEP = 10
'''
def generateSeries(base):
    first = 0 if base - STEP * 2 < 0 else base - STEP * 2
    second = 0 if base - STEP * 1 < 0 else base - STEP * 1
    fourth = base + STEP * 1
    return [first, second, base, fourth]
'''
def generateSeries(a,d):
    b=(2*a+d)/3
    c=(a+2*d)/3
    return [a,b,c,d]
def readData(fileName):
    f = open(fileName)
    data_table = []  #float table
    for line in f:
        line_list = line.split()
        data_table.append(list(map(float, line_list)))
    return data_table

def readCoords(data_table):
    coords_list = []
    for line in data_table:
        if int(line[0]) <= ROW:
            coords_list.append([line[1], line[2]])
    return coords_list

def readDemand(data_table):
    demand_list = []
    for line in data_table:
        if int(line[0]) <= ROW:
            demand_list.append(line[3])
    return demand_list

def readTime(data_table):
    time_table = []
    for line in data_table:
        if int(line[0]) <= ROW:
            time_table.append(generateSeries(line[4],line[5]))
    return time_table
    
if __name__ == '__main__':
    coords = readCoords(readData(FILENAME))
    demand = readDemand(readData(FILENAME))
    time = readTime(readData(FILENAME))
    d_c = np.array(coords)
    print(d_c)
    d_d = np.array(demand)
    print(d_d)
    d_t = np.array(time)
    print(d_t)
