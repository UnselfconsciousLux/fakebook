import facebook
import csv
import math
import pandas as pd
import numpy as np
import requests
from lxml import html
from textblob import TextBlob
import nltk

nltk.download('punkt')
token = 'EAAcEzS4nGr8BANeiWSHCQ9IrsfrtliD5mr0SLUkZCZBThD4s7UtnUrn2s31jxlbK9eh3uQGHQ6OtYRHYgw4lHZBPgAUMAvrmtOukMJPVJZA3QyajFD3dc5WIYB2tapgFrTiJrhcgKZAlkvoZCoJPLrOTunMhBg4s0ZD'
graph = facebook.GraphAPI(access_token=token, version=2.7)

df = pd.read_csv('rawData.csv')
result_df = pd.DataFrame()
result_pointer = 0

for row in df.itertuples():
    if not math.isnan(row.share_count):

        print(result_pointer)
        post_id = str(row.account_id) + "_" + str(row.post_id)
        if row.Rating == "no factual content":
            result_df.loc[result_pointer, 'Rating'] = 0
        elif row.Rating == "mostly false":
            result_df.loc[result_pointer, 'Rating'] = 0
        elif row.Rating == "mostly true":
            result_df.loc[result_pointer, 'Rating'] = 1
        if row.Category == "left":
            result_df.loc[result_pointer, 'Category'] = 0
        elif row.Category == "mainstream":
            result_df.loc[result_pointer, 'Category'] = 1
        elif row.Category == "right":
            result_df.loc[result_pointer, 'Category'] = 2

        # get the counts of likes and shares from api
        post = graph.get_object(id=post_id, fields='link,caption,description,comments')
        all_comments = ''

        try:
            for comment in post['comments']['data']:
                all_comments += comment['message']
        except:
            all_comments += ''

        blob = TextBlob(all_comments)
        polarity_sum = 0
        count = 0
        for sentence in blob.sentences:
            polarity_sum += sentence.sentiment.polarity
            count += 1
        avg_polarity = polarity_sum / row.comment_count
        result_df.loc[result_pointer, 'avg_polarity'] = avg_polarity
        result_df.loc[result_pointer, 'shareToComments'] = row.share_count / row.comment_count
        result_df.loc[result_pointer, 'ShareToReaction'] = row.share_count / row.reaction_count

        result_pointer += 1
print(result_df["Rating"], result_df["Category"], result_df["avg_polarity"], result_df["ShareToReaction"], result_df["shareToComments"])
