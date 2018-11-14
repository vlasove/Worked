from __future__ import unicode_literals
import os
import glob
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import xlsxwriter

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from tqdm import tqdm



print('\nStarting StrainReport....')
path = Path().absolute()
extension = 'xls'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('StrainReport.xlsx', engine='xlsxwriter')
workbook  = writer.book
#worksheet = workbook.add_worksheet()
cell_format = workbook.add_format({
                                   'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                    'bold': True,
                                    'fg_color': '#D7E4BC'})

col = 0
pointer = []
Square = {}

#Statistics

index_list = list()
framer = 0
col_name_stat = ['Fm.ср.знач.','Fm.ср.откл.','E.ср.знач.','E.ср.откл.','dL.ср.знач.','dL.ср.откл']
for k in result:
    index_list.append(k.split('.')[0])

statistic_frame = pd.DataFrame(data = None, index = index_list, columns = col_name_stat)

shaper = list()
    

    
for i in tqdm(result, ascii = True, desc= "Summary Part Preparation"):
    
    dataframe = pd.read_excel(i, sheet_name = 1, encoding='windows-1251', sep =';')
    df = dataframe.iloc[1:,:]
    head_list = dataframe.columns
    col_pointer = len(head_list)+1
    pointer.append(col_pointer)
    shaper.append(dataframe.shape[0])
     #Strain Replacer

    dataframe.drop(columns = ['Fразруш.','dL при разруш.'], inplace = True)
    dataframe['FmaxN'] = str()
    dataframe['FmaxN'][0] = str('N')
    dataframe['FmaxN'][1:] = dataframe['Fmax'][1:]*dataframe['S0'][1:]
    dataframe['FmaxN'][1:] = dataframe['FmaxN'][1:].astype('float64')
    dataframe = dataframe[['FmaxN','Fmax','dL при Fмакс','Eмод','S0']]
    
    
    
    Mean_list = []
    Var_list = []
    Min_list = []
    Max_list = []

    for j in dataframe.columns:
        Mean_list.append(dataframe[j][1:].mean())
        Var_list.append(sum(abs(dataframe[j][1:] - dataframe[j][1:].mean()))/dataframe[j][1:].size)
        Min_list.append(dataframe[j][1:].min())
        Max_list.append(dataframe[j][1:].max())
        
    dataframe.loc['Ср.знач.'] = Mean_list
    dataframe.loc['Ср.откл.'] = Var_list
    dataframe.loc['Min'] = Min_list
    dataframe.loc['Max'] = Max_list
   
    
    dataframe.to_excel(writer,sheet_name = 'Results_Summary', startrow= 4, startcol = 0 + col)
    
    Square_list = []
    
    for count in dataframe.iloc[1:-4,-1]:
        Square_list.append(count)
        
    Square[i] = Square_list
        
    
    col = col + 10
    
    statistic_frame.iloc[framer,:] = dataframe['Fmax'][-4], dataframe['Fmax'][-3],dataframe['Eмод'][-4],dataframe['Eмод'][-3],dataframe['dL при Fмакс'][-4],dataframe['dL при Fмакс'][-3]
    framer = framer + 1
    

#Input statistic
statistic_frame.to_excel(writer,sheet_name = 'Results_Summary', startrow= (shaper[0] + 20), startcol = 0)
    
    

worksheet = writer.sheets['Results_Summary']

cell_format = workbook.add_format({
                                   'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                    'bold': True,
                                    'fg_color': '#D7E4BC',
                                    'text_wrap':True})

# We can only write simple types to merged ranges so we write a blank string.
col = 0
k = 0
for i in result:
    worksheet.merge_range(0,0+col,3,pointer[k]+col-2, "", cell_format)

# We then overwrite the first merged cell with a rich string. Note that we
# must also pass the cell format used in the merged cells format at the end.
    worksheet.write_rich_string(0,0+col,
                            i.split('.')[0],
                            cell_format)
    col = col + 10
    k = k+1
    
    
    
#Data Part

for i in tqdm(result, ascii = True, desc= "Individual Data Preparation"):
    

    xls = pd.ExcelFile(i, on_demand = True)
    sheets = xls.sheet_names
    use_sheets = sheets[3:]
    counter = 0
    tabler = 0
    for j in use_sheets:
        dataframe_res = pd.read_excel(i, sheet_name = j, encoding='windows-1251', sep =';')
        dataframe_res.columns = dataframe_res.iloc[0,:]
        df = dataframe_res.iloc[2:,:]

        df['Напряжение'] = df.iloc[:,1]/Square[i][counter]
        #print(df.head())
        df.to_excel(writer,sheet_name = '%s'%i.split('.')[0][:30], startrow= 4, startcol = 0+tabler , index = None)

        worksheet = writer.sheets['%s'%i.split('.')[0][:30]]
        worksheet.merge_range(0,0+tabler,3,2+tabler, "", cell_format)

# We then overwrite the first merged cell with a rich string. Note that we
# must also pass the cell format used in the merged cells format at the end.
        worksheet.write_rich_string(0,0+tabler,
                            '%s'%(j),
                            cell_format)
        line_chart1 = workbook.add_chart({'type': 'scatter', 'subtype':'smooth_with_markers'})
        line_chart1.set_size({'width': 570, 'height': 350})



        #line_chart1.set_x_axis({'min':0})
        line_chart1.set_x_axis({'name':'ε,%',
                                'name_layout':{'x':0.9,'y':0.85},
                                'name_font' :{'bold': False, 'italic':False, 'size':16,'name':'TimesNewRoman'},'line':{'color':'black'},'min':0,'num_font':  {'name': 'TimesNewRoman', 'size': 14,
                                                      'major_gridlines': {'visible': 0}},
                                                     'major_tick_mark':'inside',
                                                    'minor_tick_mark':'inside'})
        line_chart1.set_y_axis({'name':'σ, Мпа',
                                'name_font' :{'bold': False, 'italic':False,'size':16,'name':'TimesNewRoman'},'line':{'color':'black'},'num_font':  {'name': 'TimesNewRoman', 'size': 14}, 
                                'major_gridlines': {'visible': 0},
                               'major_tick_mark':'inside',
                                'minor_tick_mark':'inside'})
        
        line_chart1.set_title({
    'name': '%s'%j,
    'name_font': {
        'name': 'TimesNewRoman',
        'color': 'black',
        'size' : 12,
        'bold':False,
        'italic':False
    }
})

# Configure the data series for the secondary chart.
        line_chart1.add_series({
    'categories': ['%s'%i.split('.')[0][:30], 5,0+tabler,5+df.shape[0],0+tabler],
    'values':     ['%s'%i.split('.')[0][:30], 5,2+tabler,5+df.shape[0],2+tabler],
    'line' :{'color':'black'},
    'marker':     {'type': 'circle','color':'black', 'size': 1},
    'num_format':'0,000',
    'smooth':     True,
    'data_labels':{'bold':False}
    
        })
        line_chart1.set_legend({'none': True})

#line_chart1.set_x_axis({'display_units': 'hundreds',
                  #'display_units_visible': False})

#line_chart1.set_x_axis({'interval_unit': 0.5})
#line_chart1.set_x_axis({'min':0,'max'})
#line_chart1.set_x_axis({'minor_unit': 0.4, 'major_unit': 2})

        worksheet.insert_chart(0,3+tabler, line_chart1)
        
        tabler = tabler + 12
        counter = counter +1

print("Saving...")

writer.save()

print("Done!")
