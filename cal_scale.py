#!/usr/bin/env python
# Version: 0.0
# Author: Ziwei Wu
# Purpose : to calcute C_{n}^{2}  

import xlwt
import argparse
import warnings
import numpy as np
from xlutils.copy import copy
import xlrd
import math

def readme():
    
    print "  \nNote: \n \n  It is generally accepted that the spectrum of electron density fluctuations in  the interstellar medium has a power-law form. The quantity C is a measure of turbulence along a particular line of sight, which can be calculed from the measurements of the scintillation parameters under the assumption of a Kolmogorov spectrum (Bhat et al. 1999) \n \n"

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

def write_head(filename, number):
    # open xls to rewrite data   
    old_excel = xlrd.open_workbook(filename, formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)
    freq = 124
    i = 0
    while i < 6:
        ws.write(0, number + i, str(freq) + "scale-index")
        freq += 10
        i += 1
    ws.write(0, number + 6,  "All-scale-index")

    new_excel.save(filename)
    

def function(obs_freq, distance, vdiss, mod):
    C = 2.0 * 10**(-6) * (obs_freq**(11.0/3.0)) *((distance*1000.0)**(-11.0/6.0)) *((vdiss*1000.0)**(-5.0/6.0)) * (mod**(-20.0/3.0))
    #C = 0.02 * ((obs_freq/1000.0)**(11.0/3.0)) *((distance)**(-11.0/6.0)) *((vdiss)**(-5.0/6.0)) * (mod**(-20.0/3.0))
    C =math.log(C)
    return C

def cal_scale(filename, column, distance, obsfreq, location):
    # open xls to rewrite data   
    old_excel = xlrd.open_workbook(filename, formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)

    #open xls for reading data
    data = xlrd.open_workbook(filename) 
    table = data.sheets()[0] 
    nrows = table.nrows 

    #cleaning data based on probability

    i=1
    while i<nrows:
        if str(table.cell(i,column).value) == "" or str(table.cell(i,column).value) == "nan":
            print "Jumping cell because of null value at %s, %s" % (i, column)
            ws.write(i, location, "nan")
            i += 1
        else:
            vdiss = table.cell(i,column).value
            mod = table.cell(i,column+6).value
            print obsfreq, distance, vdiss, mod
            C = function(float(obsfreq), float(distance), float(vdiss), float(mod))
            print "Calaulate Scale index at %s, %s, getting scale index is: %s" % (i, column, C)
            ws.write(i, location, C)
            i += 1



    new_excel.save(filename)



def main():
    parser = argparse.ArgumentParser(description='Select the scintillation result files.')
    parser.add_argument('files', help='The chosen files')
    parser.add_argument('-d','--distance', help='the distance based on DM with YMW16 model')
    args = parser.parse_args()
    filename = args.files
    distance = args.distance

    readme()
    ignorewarning()
    write_head(filename, 65)
    obs_freq_list = [124, 134, 144, 154, 164, 174, 153.81]
    column = 1
    location = 65
    for obsfreq in obs_freq_list:
        cal_scale(filename, column, distance, obsfreq, location)
        column += 9
        location += 1

if  __name__=="__main__":
    main()
