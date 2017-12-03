# Save Model Using joblib
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import facebook
import os
import csv
import pandas as pd
import numpy as np
import codecs
import math
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
str1 = "adam"
# str1 = unicode(str1, errors='ignore')
dataframe = pd.read_csv(str1)
df = pd.read_csv(str1)
NDF = pd.DataFrame()
# result_pointer = 0

# for row in df.itertuples():
#     NDF.loc[result_pointer, 'Rating'] = row.Rating
#     if not math.isnan(row.num_shares):
#         if row.num_comments > 0:
#             NDF.loc[result_pointer, 'shareToComments'] = row.num_shares / row.num_comments
#         else:
#             NDF.loc[result_pointer, 'shareToComments'] = row.num_shares

#         if row.num_reactions > 0:
#             NDF.loc[result_pointer, 'ShareToReaction'] = row.num_shares / row.num_reactions
#         else:
#             NDF.loc[result_pointer, 'ShareToReaction'] = row.num_shares
#         result_pointer += 1
#         NDF.loc[result_pointer, 'Category'] = row.Category
# print('DateFrame:')
# print(NDF)

# print(NDF.isnull().sum())

# X_train, X_test, y_train, y_test = train_test_split(NDF.loc[:, "Category":"ShareToReaction"], NDF["Rating"], test_size=0.2, random_state=42)
# loaded_model.fit(X_train, y_train)
# # filename = 'finalized_model2.sav'
# # pickle.dump(loaded_model, open(filename, 'wb'))
# y_pred = loaded_model.predict(X_test)
# print("***********************")
# print(y_pred)
# print("***********************")


token = 'EAAcEzS4nGr8BANeiWSHCQ9IrsfrtliD5mr0SLUkZCZBThD4s7UtnUrn2s31jxlbK9eh3uQGHQ6OtYRHYgw4lHZBPgAUMAvrmtOukMJPVJZA3QyajFD3dc5WIYB2tapgFrTiJrhcgKZAlkvoZCoJPLrOTunMhBg4s0ZD'
graph = facebook.GraphAPI(access_token=token, version=2.7)


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print(request)
    content = request.data
    print(content)
    return "Hello"


@app.route('/index', methods=['GET', 'POST'])
def index():
    # for filename in os.listdir('Data'):
    #     filename = 'Data/' + filename
    results = ''
    posts_file = open('Data/final.csv')
    # post_reader = csv.reader(posts_file)
    # post = pd.read_csv(filename)
    for row in posts_file:
        results = results + row
    # for row in post_reader:
    #     results.append(row)
    posts_file.close()
    return results


if __name__ == '__main__':
    print("Server is up.")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
