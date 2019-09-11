import xlrd
import numpy as np 
from matplotlib import pyplot as plt 
import argparse
import warnings

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

def get_fit_data(filename,i,factor):
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(u'My Worksheet')

    data_list = []
    data_err_list = []
    mjd = []
    ncow = 1
    
    a=int(table.nrows) - 1
    
    while ncow < a: 
        if table.cell(ncow,i).value == '' or str(table.cell(ncow,i).value) == "nan":
            ncow = ncow+1
        else:
            mjd.append(table.cell(ncow,0).value-57100)
            data_list.append(table.cell(ncow,i).value*factor)
            data_err_list.append(table.cell(ncow,i+1).value*factor)
            #print i, ncow,table.cell(ncow,i).value
            ncow = ncow+1


    return data_list, data_err_list, mjd


def plotdata(i, filename, factor):
    #loading data from excel for time-scale
    j = 0
    freq = 124
    marker_list = ['*', '+', 'd', 'v', '4', '1']
    color_list = ['red', 'blue', 'orange', 'green', 'black', 'yellow']
    line_style_list = ['dotted', 'dashdot', 'solid', 'dotted', 'dashed', 'dashdot']
    while i < 54:
        freqname = str(freq) + 'Hz'
        time_list, time_err_list, mjd = get_fit_data(filename, i, factor)
        plt.errorbar(mjd,time_list, yerr=time_err_list,color=color_list[j], label=freqname, linestyle=line_style_list[j], fmt='none', marker=marker_list[j], capsize=2)
        freq += 10
        i += 9
        j += 1

def plotspectra(filename, number):
    data_list, data_err_list, mjd = get_fit_data(filename, number, 1)

def main():
    parser = argparse.ArgumentParser(description='Select the scintillation result files.')
    parser.add_argument('files', help='The chosen files')
    parser.add_argument('-t','--type', help='which paras do you want to plot: time, bandwidth, curvature, spectratime, spectrafrequency and scalingfactor')
    args = parser.parse_args()
    filename=args.files
    plottype=args.type

    ignorewarning()

    fig, ax = plt.subplots(dpi=100)
    if plottype == 'time':
        column = 4
        times = 1
        ytitle = "Time-scale (mins)"
        plotdata(column, filename, times)
        plt.ylabel(ytitle,fontsize=15)
    elif plottype == 'bandwidth':
        column = 1
        times = 1000
        ytitle = "Frequency bandwith (Khz)"
        plotdata(column, filename, times)
        plt.ylabel(ytitle,fontsize=15)
    elif plottype== "curvature":
        column = 8
        times = 1
        ytitle = "Curvature"
        plotdata(column, filename, times)
        curvature, cur_err, mjd = get_fit_data(filename, 80, 1)
        #print curvature, cur_err, mjd
        #plt.errorbar(mjd, curvature, yerr=cur_err)
        plt.ylabel(ytitle,fontsize=15)
        plt.ylim(0,1.5)
        #plt.xlim(-50, 150)
    elif plottype == 'spectratime':
        ytitle = 'scale index at time-scale'
        data_list, data_err_list, mjd = get_fit_data(filename, 73, 1)
        plt.errorbar(mjd,data_list,yerr=data_err_list, fmt='o')
        plt.plot([0,1400], [4.4, 4.4], label='Kolmogorov spectrum with 4.4', linestyle='--')
        plt.plot([np.min(mjd),np.max(mjd)],[np.mean(data_list),np.mean(data_list)])
        ax.fill_between(mjd, np.mean(data_list)+np.mean(data_err_list), np.mean(data_list)-np.mean(data_err_list), alpha=.25, label='1-sigma interval')
        plt.ylabel(ytitle,fontsize=15)
    elif plottype == 'spectrafrequency':
        ytitle = 'scale index at frequency-bandwidth'
        data_list, data_err_list, mjd = get_fit_data(filename, 75, 1)
        plt.errorbar(mjd,data_list,yerr=data_err_list, fmt='o')
        plt.plot([np.min(mjd),np.max(mjd)],[np.mean(data_list),np.mean(data_list)])
        plt.plot([0,1400], [1.2, 1.2], label='Kolmogorov spectrum with 1.2', linestyle='--')
        ax.fill_between(mjd, np.mean(data_list)+np.mean(data_err_list), np.mean(data_list)-np.mean(data_err_list), alpha=.25, label='1-sigma interval of mean value')
        plt.ylabel(ytitle,fontsize=15)
    elif plottype == 'scalingfactor':      
        i = 0
        freq = 124
        number = 65
        while i < 6:
            data_list, data_err_list, mjd = get_fit_data(filename, number, 1)
            print len(mjd)
            plt.plot(mjd,data_list, linestyle='--', label = str(freq)+'MHz')
            freq += 10
            number += 1
            i += 1
 
    else:
       print ('Please input the right string')


    plt.legend(loc='up right')
    #plt.xlim(0,600)
    plt.title('J1136+1551')
    plt.xlabel("MJD after 57100",fontsize=20)
    plt.subplots_adjust(bottom=0.14, right=0.97, top=0.90, left=0.11)
    plt.show()
    #plt.savefig('J1136+1551-curvature.png', dpi=200)

if  __name__=="__main__":
    main()
