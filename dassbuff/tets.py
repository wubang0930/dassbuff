# -*- coding: utf-8 -*-
# @Author: fangbei
# @Date:   2017-08-26

import re
import json
import requests
from bs4 import BeautifulSoup


file=open('dassbuff/data/handtag.html','r',encoding='utf-8')

soup=BeautifulSoup(file,'html.parser')
divs=soup.find_all('div')

start_flag=False
for div in divs:
    if div.text.find('手牌')!=-1:
        start_flag=True
        continue
    print(div.text)
