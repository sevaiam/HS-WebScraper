import requests
from bs4 import BeautifulSoup
import string
import os

page_no = int(input())
art_type = input()
for i in range(page_no):
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'}, params={'page': i+1})
    dir_name = f'Page_{i+1}'
    os.mkdir(dir_name)
    os.chdir(dir_name)
    soup = BeautifulSoup(r.content, 'html.parser')

    news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=art_type) # replace <article_type>

    punct = string.punctuation
    for news_article in news_article_links:
        anchor = news_article.find_parent('article').find('a', {'data-track-action': 'view article'})
        title = anchor.text
        for i in title:
            if i in punct:
                title = title.replace(i, "")
            if i in ' ':
                title = title.replace(i, "_")

        filename = str(title) + '.txt'

        link_short = anchor.get('href')
        link = f'https://www.nature.com{link_short}'
        art_request = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
        art_content = BeautifulSoup(art_request.content, 'html.parser')
        content = art_content.find('div', {'class':'c-article-body'})
        # print(content.text)
        with open(filename, 'wb') as file:
               file.write(bytes(content.text, encoding='utf-8'))

    os.chdir('..')