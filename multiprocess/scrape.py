from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def dienbienkhoplenh(ma_ck, date):
    request = requests.get("https://s.cafef.vn/Lich-su-giao-dich-{}-6.chn?date={}".format(ma_ck, date),
                            verify=False)
    soup = BeautifulSoup(request.content, "lxml")
    table = soup.find_all("table", {"id" : "tblData"})
    df = pd.read_html(str(table))[0]
    df.columns = ["Thời gian", "Giá", "Khối lượng lô", "Khối lượng tích luỹ", "Tỷ trọng"]
    return df


def khoplenh(ls_mack, from_date, end_date):
    datalist = []
    for mack in ls_mack:
        for date in pd.date_range(from_date, end_date):
            try:
                df = dienbienkhoplenh(mack, pd.datetime.strftime(date, '%d/%m/%Y'))
                df["Mã chứng khoán"] = mack
                df["Ngày"] = date
                datalist.append(df)
            except ValueError:
                print("{}: Không có giao dịch ngày {}".format(mack, date))
    result = pd.concat([datalist[i] for i in range(len(datalist))], ignore_index=True)
    return result
