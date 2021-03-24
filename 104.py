import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# 指定頁數給while用
page = 1
# 建立空list給pandas用,pandas 寫入csv的第一個參數可以是list,dict
# 要在迴圈最外面,如果放在while裡面,裡面的資料會一直被覆蓋掉
values = []

while page <10:
    # f"",f指的是格式化,字串被{}包起來的會被視為變數,python 3.6 版本以上的新增功能
    # 同樣的,可以把keyword=Python的python用{}包起來,這樣就可以用input功能,讓使用者輸入她想找的關鍵字職缺
    url = f"https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=Python&order=15&asc=0&page={page}&mode=s&jobsource=2018indexpoc"
    # 顯示目前頁數,不然不知道現在再爬哪一頁
    print("目前頁數 : ",page)
    resp = requests.get(url)
    # lxml 是解析器的一種,用老師教的也可以
    soup = BeautifulSoup(resp.text,"lxml")
    # 我比較習慣find,結果跟select 是一樣的,先在網頁找到資料位於哪一個div,在一層一層的往div內部取得要的資料
    # 先定位你要的資料位在哪一個div,id 是什麼,用find找出(id在html語法內是唯一,不能重複,所以有id,就id優先,不會有重複的問題)
    # 定位完後,往內找你要的資料在哪一個標籤內
    soup2 = soup.find('div',{'id':'js-job-content'}).findAll('article',{'class':'b-block--top-bord job-list-item b-clearfix js-job-item'})
    # 用for 依序讀出每一筆資料,在每一筆資料內在找出要的資料
    for job in soup2:
        # .text 取標籤內的文字,取完文字後因為有前後很多空白,用 .strip()把空白都拿掉
        update_date = job.find('span', {'class': 'b-tit__date'}).text.strip()
        # 因為底下有些資料會沒有,所以用try 出錯時讓他跑except
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
        # job 內還有其他資料,要的話可以加在以下,最後的columns要添加欄位,要跟你的資料個數是一致的
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
# 建立空DataFrame()
df = pd.DataFrame()
# 指定欄位名稱
columns = ['公司名稱','公司類別描述','職缺名稱','職務性質','職務內容','更新日期', '職缺連結','公司地址','地區','經歷','學歷']
# 依序放入參數,也接受放入字典,放入字典就不用放values,columns,但要多一步驟,把values,columns組合成字典
# df = pd.DataFrame(dict)
df = pd.DataFrame(values, columns=columns)
# 第一個參數是檔名,因為沒有指明路徑要放在哪,所以會存在當前目錄底下,存csv會亂碼,"utf-8"沒用,所以改用encoding="utf_8_sig",編碼後存入
# 如果不存csv,存成一般excel,xlsx檔就不用encoding="utf_8_sig"
df.to_csv("104_list.csv",encoding="utf_8_sig")