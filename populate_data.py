import facebook
import csv
import math
import pandas as pd
import numpy as np
import requests
# from lxml import html
from textblob import TextBlob
import nltk
from sklearn import linear_model
from sklearn.model_selection import train_test_split

nltk.download('punkt')
token = 'EAAcEzS4nGr8BANeiWSHCQ9IrsfrtliD5mr0SLUkZCZBThD4s7UtnUrn2s31jxlbK9eh3uQGHQ6OtYRHYgw4lHZBPgAUMAvrmtOukMJPVJZA3QyajFD3dc5WIYB2tapgFrTiJrhcgKZAlkvoZCoJPLrOTunMhBg4s0ZD'
graph = facebook.GraphAPI(access_token=token, version=2.7)

df = pd.read_csv('rawData.csv')
result_df = pd.DataFrame()
result_pointer = 0

for row in df.itertuples():
    if not math.isnan(row.share_count):

        post_id = str(row.account_id) + "_" + str(row.post_id)
        if row.Rating == "no factual content":
            result_df.loc[result_pointer, 'Rating'] = 0
        elif row.Rating == "mostly false":
            result_df.loc[result_pointer, 'Rating'] = 0
        elif row.Rating == "mostly true":
            result_df.loc[result_pointer, 'Rating'] = 1
        elif row.Rating == "mixture of true and false":
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
        if row.comment_count > 0:
            result_df.loc[result_pointer, 'avg_polarity'] = polarity_sum / row.comment_count
            result_df.loc[result_pointer, 'shareToComments'] = row.share_count / row.comment_count
        else:
            result_df.loc[result_pointer, 'avg_polarity'] = polarity_sum
            result_df.loc[result_pointer, 'shareToComments'] = row.share_count

        if row.reaction_count > 0:
            result_df.loc[result_pointer, 'ShareToReaction'] = row.share_count / row.reaction_count
        else:
            result_df.loc[result_pointer, 'ShareToReaction'] = row.share_count
        result_pointer += 1
print(result_df)

print(result_df.isnull().sum())


# Making the logistic Regression Model
logreg = linear_model.LogisticRegression(C=1e5)
X_train, X_test, y_train, y_test = train_test_split(result_df.loc[:, "Category":"ShareToReaction"], result_df["Rating"], test_size=0.2, random_state=42)
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print(y_pred)
score = logreg.score(X_test, y_test)
print(score * 100)
