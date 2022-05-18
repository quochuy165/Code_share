import os
#set dir
os.chdir('folder_path') #Điền đường dẫn chưa folder file scrape.py
##import
from multiprocessing import Pool
import scrape
import requests
import numpy as np
import pandas as pd


#Set number of process
n_process = 4 #Thay đổi số core
#set pool
pool = Pool(n_process)
#device list stock
list_ck = ['FPT', 'TCB', 'HPG', 'HSG', 'MBB', 'BSI', 'CTG', 'VPB'] #Thay đổi danh sách mã ck

ls = [i.tolist() for i in np.array_split(list_ck, n_process)]
startdate = ['2020-01-15']*n_process #Thay đổi ngày bắt đầu
enddate = ['2020-02-15']*n_process  #Thay đổi ngày kết thúc
#concat argument
args = zip(ls, startdate, enddate)

##Run
if __name__ == '__main__':
    dfs = pool.starmap(scrape.khoplenh, args)
    df_all = pd.concat(dfs, ignore_index=True)
