# Analysis_scintillation
This Python code script is wrote by Ziwei to analyze scintillation parameters.
The first step run:
    python ../analysis_scintillation/combine_data_into_xls.py -m J0837+0610-all.txt -d 0.72 -f 2.0 *4.txt
The second step run:
    python ../analysis_scintillation/cal_scale.py Excel_Workbook.xls -d 0.72
The third step run:
    python ../analysis_scintillation/cal_spectra_index.py Excel_Workbook.xls
Then, you can have some plots:
    a. python plot_scitillnation_para.py -t 'bandwidth' ../J0837+0610/Excel_Workbook.xls
    b. python plot_scitillnation_para.py -t 'time' ../J0837+0610/Excel_Workbook.xls
    c. python plot_scitillnation_para.py -t 'time' ../J0837+0610/Excel_Workbook.xls
    d. python plot_scitillnation_para.py -t 'spectrafrequency' ../J0837+0610/Excel_Workbook.xls
