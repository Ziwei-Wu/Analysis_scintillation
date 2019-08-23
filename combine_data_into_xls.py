import xlwt
import argparse
import warnings
import numpy as np
from xlutils.copy import copy
import xlrd
import math

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

#first, creating a excel, and input MJD from mianfile
def creat_excel(number,mainfilename):
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    worksheet.write(0, 0, 'MJD')
    i=1
    j=1
    obfreq=str(124)
    while i<(number*9+1):
        worksheet.write(0, i, obfreq+'freq')
        worksheet.write(0, i+1, obfreq+'freq-err')
        worksheet.write(0, i+2, 'probability')
        worksheet.write(0, i+3, obfreq+'time')
        worksheet.write(0, i+4, obfreq+'time-err')
        worksheet.write(0, i+5, 'probability')
        worksheet.write(0, i+6, obfreq+'modulation index')
        worksheet.write(0, i+7, obfreq+'curvature')
        worksheet.write(0, i+8, obfreq+'curvature-err')
        i=(j*9)+1
        j=j+1
        obfreq=int(obfreq)+10
        obfreq=str(obfreq)

    #for all frequency range
    i = 55
    worksheet.write(0, i, 'All-freq')
    worksheet.write(0, i+1, 'ALL-freq-err')
    worksheet.write(0, i+2, 'probability')
    worksheet.write(0, i+3, 'ALL-time')
    worksheet.write(0, i+4, 'ALL-time-err')
    worksheet.write(0, i+5, 'probability')
    worksheet.write(0, i+6, 'ALL-modulation index')
    worksheet.write(0, i+7, 'ALL-curvature')
    worksheet.write(0, i+8, 'ALL-curvature-err')

    workbook.save('Excel_Workbook.xls')

    f = np.genfromtxt('%s' % mainfilename)

    old_excel = xlrd.open_workbook('Excel_Workbook.xls', formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)
    i=1
    full_mjd_list = []
    while i<(len(f)+1):
        ws.write(i,0,f[i-1][4])
        full_mjd_list.append(f[i-1][4])
        i=i+1
    
    new_excel.save('Excel_Workbook.xls')

    return len(f), full_mjd_list

#put all data into this xls
def write_data(filename, full_mjd_list,number):

    f = np.genfromtxt('%s' % filename)

    old_excel = xlrd.open_workbook('Excel_Workbook.xls', formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)
    i=0
    j=0
 
    while i<len(f):
        while j<len(full_mjd_list):
            if full_mjd_list[j] == f[i][4]:
                ws.write(j+1,number,f[i][0])
                ws.write(j+1,number+1,f[i][1])
                ws.write(j+1,number+2,f[i][10]) 
                ws.write(j+1,number+3,f[i][2]) 
                ws.write(j+1,number+4,f[i][3])
                ws.write(j+1,number+5,f[i][11]) 
                ws.write(j+1,number+6,f[i][12]) 
                ws.write(j+1,number+7,f[i][7]) 
                ws.write(j+1,number+8,f[i][8]) 
            j=j+1
        j=0
        i=i+1
    
    new_excel.save('Excel_Workbook.xls')


def clean_probability(datalens, column):
    # open xls to rewrite data   
    old_excel = xlrd.open_workbook('Excel_Workbook.xls', formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)

    #open xls for reading data
    data = xlrd.open_workbook('Excel_Workbook.xls') 
    table = data.sheets()[0] 

    #cleaning data based on probability
    i=1
    while i<(datalens+1):
        if table.cell(i,column).value == '' or table.cell(i,column).value == "nan":
            print "cleaning data because of null vale at %s, %s" % (i, column)
            ws.write(i, column-2, "nan")
            ws.write(i, column-1, "nan")
            ws.write(i, column, "nan")
            i += 1
        elif table.cell(i,column).value < 0.9 or table.cell(i,column).value > 1.1:
            print "cleaning data at %s %s with probality: %s" % (i, column,table.cell(i,column).value)
            ws.write(i, column-2, "nan")
            ws.write(i, column-1, "nan")
            ws.write(i, column, "nan")
            i += 1

        else:
            i += 1

    new_excel.save('Excel_Workbook.xls')

def clean_size(datalens, column, factor):
    # open xls to rewrite data   
    old_excel = xlrd.open_workbook('Excel_Workbook.xls', formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)

    #open xls for reading data
    data = xlrd.open_workbook('Excel_Workbook.xls') 
    table = data.sheets()[0] 

    #cleaning data based on size
    #get mean value
    i = 1
    data_list = []
    while i<(datalens+1):
        if table.cell(i,column).value == '' or str(table.cell(i,column).value) == "nan":
            i += 1
        else:    
            data_list.append(table.cell(i,column).value)
            i += 1 

    threshold = factor * np.mean(data_list) 

    #clean data
    i = 1
    while i<(datalens+1):
        if table.cell(i,column).value == '' or str(table.cell(i,column).value) == "nan":
            i += 1
        elif table.cell(i,column).value > threshold:
            print "cleaning data at %s, %s because of unphysical value: %s." % (i, column, table.cell(i,column).value)
            ws.write(i,column, "nan")
            ws.write(i,column+1, "nan")
            ws.write(i,column+2, "nan")
            i += 1
        else:
            i += 1  

    new_excel.save('Excel_Workbook.xls') 
        

def main():
    parser = argparse.ArgumentParser(description='Select the scintillation result files.')
    parser.add_argument('files', nargs='+', help='The chosen files')
    parser.add_argument('-m','--mainfiles', help='The chosen main files')
    parser.add_argument('-d','--inputdistance', type=float, help='The distance of the input pulsar in the unit of kpc')
    parser.add_argument('-f','--factor', type=float, help='The cleaning factor')
    args = parser.parse_args()


    mainfilename=args.mainfiles
    distance=args.inputdistance
    filename=args.files
    factor=args.factor

    filename.append(mainfilename)

    #put data into .xls file
    len_f, full_mjd_list = creat_excel(6,mainfilename)
    number = 1
    for scale_file in filename:
        write_data(scale_file, full_mjd_list,number)
        number=number+9

    #cleaning data based on fitting probability
    location_list = [3, 6, 12, 15, 21, 24, 30, 33, 39, 42, 48, 51, 57, 60]
    for location in location_list:
        clean_probability(len(full_mjd_list), location)

    #cleaning data based on size
    location_list = [1, 4, 10, 13, 19, 22, 28, 31, 37, 40, 46, 49, 55, 58]
    for location in location_list:
        clean_size(len(full_mjd_list), location, factor)

if  __name__=="__main__":
    ignorewarning()
    main()
