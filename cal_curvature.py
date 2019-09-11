#!/usr/bin/env python
# Version: 0.0
# Author: Ziwei Wu
# Purpose : to calcute spectra index 

import xlwt
import argparse
import warnings
import numpy as np
from xlutils.copy import copy
import xlrd
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def read():    
    print ("  \nNote: \n \n  The scintillation arc curvature is excepted evolve with frequency according to a power law  curvature ~ v**{-2}\n \n")

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

def write_head(filename, number):
    # open xls to rewrite data   
    old_excel = xlrd.open_workbook(filename, formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)
    ws.write(0, number,  "curvature-frequency")
    ws.write(0, number+1,  "error")

    new_excel.save(filename)

def func_powerlaw(x, m, k):
    return k*x**m

def fitdata(xdata, ydata, ydataerror):
    popt, pcov = curve_fit(func_powerlaw, xdata, ydata, sigma=ydataerror, maxfev=10000)
    perr = np.sqrt(np.diag(pcov))
    return popt[0], perr[0]


def getdata(filename, firstnumber, jump, location):
    # open xls to rewrite data   
    old_excel = xlrd.open_workbook(filename, formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)

    #open xls for reading data to get observation number
    data = xlrd.open_workbook(filename) 
    table = data.sheets()[0] 
    nrows = table.nrows 

    #get fit data
    i=1

    column = firstnumber
    while i<nrows:
        data_list = []
        data_err_list = []
        obsfreq = 124
        obsfreq_list = []
        while column < 54:
            if str(table.cell(i,column).value) == "" or str(table.cell(i,column).value) == "nan" or float(table.cell(i,column).value) >= 2.0:
                print "Jumping cell because of null value at %s, %s" % (i, column)
                column += jump
                obsfreq += 10
            else:
                data = table.cell(i,column).value
                data_err = table.cell(i,column+1).value
                data_list.append(data)
                data_err_list.append(data_err)
                obsfreq_list.append(obsfreq)
                column += jump
                obsfreq += 10

        #fit data only if len(data) >= 2
        if len(data_list) >= 3:
            print obsfreq_list, data_list, data_err_list
            para, paraerr = fitdata(obsfreq_list, data_list, data_err_list)
            ws.write(i, location, para)
            ws.write(i, location+1, paraerr)
        else:
            ws.write(i, location, "nan")
            ws.write(i, location+1, "nan")


        i += 1
        column = firstnumber

    new_excel.save(filename)


def main():
    parser = argparse.ArgumentParser(description='Select the scintillation result files.')
    parser.add_argument('files', help='The chosen files')
    args = parser.parse_args()
    filename = args.files

    write_head(filename, 80)
    getdata(filename, 8, 9, 80)

if  __name__=="__main__":
    read()
    ignorewarning()
    main()
