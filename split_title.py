import requests
from bs4 import BeautifulSoup
import jieba
import jieba.analyse

base_url = 'https://www.niar.org.tw'
news_base_url = 'https://www.niar.org.tw/xmdoc?xsmsid=0I148622737263495777'

page = 1
news_count = 0

print("國家實驗研究院新聞列表：\n")

while True:
    url = f"{news_base_url}&page={page}"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')

    found_news = False

    for row in rows:
        date_td = row.find('td', class_='date')
        title_td = row.find('td', class_='title')
        
        if date_td and title_td:
            found_news = True
            news_count += 1
            date = date_td.text.strip()
            a_tag = title_td.find('a')
            title = a_tag.text.strip()
            tags = jieba.analyse.extract_tags(title, topK=10)  
            link = base_url + a_tag['href']
            print(f"{news_count}. [{date}] {title}\n   {tags}\n   👉 {link}\n")

    if not found_news:
        break  # 沒有新內容就停止
    page += 1
