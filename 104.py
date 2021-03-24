import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

page = 1
values = []

while page <10:
    url = f"https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=Python&order=15&asc=0&page={page}&mode=s&jobsource=2018indexpoc"
    print("目前頁數 : ",page)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"lxml")
    soup2 = soup.find('div',{'id':'js-job-content'}).findAll('article',{'class':'b-block--top-bord job-list-item b-clearfix js-job-item'})
    for job in soup2:
        update_date = job.find('span', {'class': 'b-tit__date'}).text
        update_date = re.sub('\r|\n| ', '', update_date)
        try:
            address = job.select('ul > li > a')[0]['title']
            address = re.findall('公司住址：(.*?)$', address)[0]
            jobLink = "https:" + job.find('a', {'class': 'js-job-link'})['href']
        except:
            address = ''

        loc = job.find('ul', {'class': 'b-list-inline b-clearfix job-list-intro b-content'}).findAll('li')[0].text
        exp = job.find('ul', {'class': 'b-list-inline b-clearfix job-list-intro b-content'}).findAll('li')[1].text
        try:
            edu = job.find('ul', {'class': 'b-list-inline b-clearfix job-list-intro b-content'}).findAll('li')[2].text
        except:
            edu = ''

        try:
            content = job.find('p').text
        except:
            content = ''
        try:
            tags = [tag.text for tag in soup2[0].find('div', {'class': 'job-list-tag b-content'}).findAll('span')]
        except:
            tags = []
        value = [job['data-cust-name'],  # 公司名稱
                 job['data-indcat-desc'],  # 公司類別描述
                 job['data-job-name'],  # 職缺名稱
                 job['data-job-ro'],  # 職務性質 _判斷全職兼職 1全職/2兼職/3高階/4派遣/5接案/6家教
                 content,  # 職務內容
                 update_date,  # 更新日期
                 jobLink,  # 職缺連結
                 address,  # 公司地址
                 loc,  # 地區
                 exp,  # 經歷
                 edu  # 學歷
                 ]
        values.append(value)
    page = page + 1

df = pd.DataFrame()
columns = ['公司名稱','公司類別描述','職缺名稱','職務性質','職務內容','更新日期', '職缺連結','公司地址','地區','經歷','學歷']

df = pd.DataFrame(values, columns=columns)
df.to_csv("104_list.csv",encoding="utf_8_sig")