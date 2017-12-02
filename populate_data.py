import facebook
import csv
import pandas as pd
import numpy as np
import requests
from lxml import html
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk

nltk.download('punkt')


def getlikescount(post, graph):
    count = 0
    id = post['id']
    if 'likes' in post:
        likes = post['likes']
        while(True):
            count = count + len(likes['data'])
            if 'paging' in likes and 'after' in likes['paging']['cursors']:
                likes = graph.get_connections(id, 'likes', after=likes['paging']['cursors']['after'])
            else:
                break
        return count
    else:
        return 0


token = 'EAAcEzS4nGr8BANeiWSHCQ9IrsfrtliD5mr0SLUkZCZBThD4s7UtnUrn2s31jxlbK9eh3uQGHQ6OtYRHYgw4lHZBPgAUMAvrmtOukMJPVJZA3QyajFD3dc5WIYB2tapgFrTiJrhcgKZAlkvoZCoJPLrOTunMhBg4s0ZD'
graph = facebook.GraphAPI(access_token=token, version=2.7)

df = pd.read_csv('rawData.csv')

for row in df.itertuples():
    post_id = str(row.account_id) + "_" + str(row.post_id)
    if row.Rating == "no factual content":
        df.loc[row.Index, 'Rating'] = 0
    elif row.Rating == "mostly true":
        df.loc[row.Index, 'Rating'] = 1
    elif row.Rating == "mostly false":
        df.loc[row.Index, 'Rating'] = 2
    if row.Category == "left":
        df.loc[row.Index, 'Category'] = 0
    elif row.Category == "mainstream":
        df.loc[row.Index, 'Category'] = 1
    elif row.Category == "right":
        df.loc[row.Index, 'Category'] = 2
    url = "https://facebook.com/" + post_id
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    # tree = html.fromstring(r.content)
    # buyers = tree.xpath('//a[@class="UFIShareLink"]/text()')
    # mydivs = soup.find_all("a", class_="UFIShareLink")
    # print(mydivs)
    # print(soup)

    # get the counts of likes and shares from api
    post = graph.get_object(id=post_id, fields='link,caption,description,comments')
    all_comments = ''
    for comment in post['comments']['data']:
        all_comments += comment['message']
    blob = TextBlob(all_comments)

    polarity_sum = 0
    count = 0
    for sentence in blob.sentences:
        # print(sentence)
        polarity_sum += sentence.sentiment.polarity
        count += 1
        # print(sentence.sentiment.polarity)

    avg_polarity = polarity_sum / count
    print(avg_polarity)
    # likes = post['likes']['summary']['total_count']
    # shares = post['shares']['summary']['total_count']
    # print(post_id, " ", post['reactions']['summary']['total_count'])
    # print(post_id, " ", post['reactions']['summary']['viewer_reaction'])
# print(graph.get_object(id=post_id))
