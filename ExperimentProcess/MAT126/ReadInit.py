# -*- coding: utf-8 -*-
import re
import numpy as np
from xml.etree import ElementTree as ET
import GlobalVariables
import os

p = re.compile(u"\s+")

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

    
def read_xml(file_name):
    """
    """
    per=ET.parse(file_name)
    
    root = per.getroot()
    #GlobalVariables.
    #ybcrs = np.array([0, 0, 0, 0])
    #Ys=per.findall(u"./YBC/Bend/Y")
    X = root.find(u"X")
    for node in X.iter(u"PARAM"):
        GlobalVariables.s_2100 = float(node.find(u"S").text)
        GlobalVariables.c_2100 = float(node.find(u"C").text)
        GlobalVariables.n_2100 = float(node.find(u"N").text)
        GlobalVariables.t_2100 = float(node.find(u"T").text) 
    
    Y = root.find("Y")
    for node in Y.iter(u"PARAM"):
        GlobalVariables.s_2200 = float(node.find(u"S").text)
        GlobalVariables.c_2200 = float(node.find(u"C").text)
        GlobalVariables.n_2200 = float(node.find(u"N").text)
        GlobalVariables.t_2200 = float(node.find(u"T").text) 

    Z = root.find("Z")
    for node in Z.iter(u"PARAM"):
        GlobalVariables.s_2300 = float(node.find(u"S").text)
        GlobalVariables.c_2300 = float(node.find(u"C").text)
        GlobalVariables.n_2300 = float(node.find(u"N").text)
        GlobalVariables.t_2300 = float(node.find(u"T").text) 
    
    return

read_xml("init.xml") 