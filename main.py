# Save Model Using joblib
import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
from flask import Flask
from flask_cors import CORS
import facebook
import os
import csv

app = Flask(__name__)
CORS(app)

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

token = 'EAAcEzS4nGr8BANeiWSHCQ9IrsfrtliD5mr0SLUkZCZBThD4s7UtnUrn2s31jxlbK9eh3uQGHQ6OtYRHYgw4lHZBPgAUMAvrmtOukMJPVJZA3QyajFD3dc5WIYB2tapgFrTiJrhcgKZAlkvoZCoJPLrOTunMhBg4s0ZD'
graph = facebook.GraphAPI(access_token=token, version=2.7)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    content = requests.json
    print(content)
    return "Hello"

@app.route('/index', methods=['GET', 'POST'])
def feed():
    results = {}
    for filename in os.listdir('Data'):
        filename = 'Data/' + filename
        posts_file = open(filename)
        reader = csv.reader(posts_file)
        for row in reader:
            results.append(row)
        posts_file.close()
    return results

if __name__ == '__main__':
    print("Server is up.")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
