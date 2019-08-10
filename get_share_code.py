from urllib.request import urlopen
from bs4 import BeautifulSoup as bts
import re
import pandas as pd
import datetime


url = 'https://zh.wikipedia.org/wiki/%E6%B2%AA%E6%B7%B1300'

target_html = urlopen(url).read().decode('utf-8')

soup = bts(target_html,'lmxl')

target_table = soup.find('table')

CSI300_trs = target_table.find_all('tr')[1:]

target_data = []

for i in CSI300_trs:
	CSI300_tds = i.find_all('td')
	share_code =CSI300_tds[0].get_text()
	share_name = CSI300_tds[1].get_text()
	exchange = CSI300_tds[3].get_text()
	target_data.append([share_code, share_name, exchange])

CSI300_data =pd.DataFrame(target_data,colunms=['share_code', 'share_name', 'Exchange'])

date = datetime.date.today().strftime('%Y%m%d')

CSI300_data.to_csv(f'CSI300_{date}',encoding='utf_8_sig')

