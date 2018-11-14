import numpy as np
import pandas as pd
import os

def readElement(cwd):
    fileNames = os.listdir(cwd)
    if not ('1.csv' in fileNames and '2.csv' in fileNames and '3.csv' in fileNames):
        raise ValueError('error')
    sigma1 = pd.read_csv('1.csv')
    sigma2 = pd.read_csv('2.csv')
    sigma3 = pd.read_csv('3.csv')
    
    clearedData = pd.ExcelWriter('clearedData.xlsx')