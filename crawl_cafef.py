from bs4 import BeautifulSoup
import pandas as pd
import requests

def dienbienkhoplenh(ma_ck, date):
    request = requests.get("https://s.cafef.vn/Lich-su-giao-dich-{}-6.chn?date={}".format(ma_ck, date))
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

df = khoplenh(["FPT", "MBB", "ABC"], from_date="2020-01-15", end_date="2020-03-10")

#Set index
df['Time'] = pd.to_datetime(df['Ngày'].astype(str) + ' ' + df['Thời gian'], format='%Y-%m-%d %H:%M:%S')
df.index = df['Time']
###Resample time
df = df.groupby(['Mã chứng khoán', 'Ngày']).resample('30T', label='right', closed='right')['Khối lượng tích luỹ', 'Giá'].ffill().reset_index().\
    dropna()
df.head()
