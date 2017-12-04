_ All of the code is also on github: _ [link](https://github.com/abouelkhair5/fakebook)

## Inspiration
In the current political climate and the widespread issue of fake news on social media, we found it imperative for this problem to be solved. There needs to be quick, reliable flagging of potentially malicious posts that try to deceive other social-media users. By flagging the posts early using machine learning without the input of other users, as is the current system on Facebook, the algorithm produces faster results. This was the inspirational idea for us to pursue the fake news challenge.

##What it does
Fakebook uses advanced linear-regression machine learning algorithms to directly flag users and posts that are used to spread deceiving information. The process used in the demo is relatively simple, in that we upload a facebook user account to a custom web app, and the web app pushes the data crawled from the account using the facebook api to the machine learning algorithm. This algorithm in turn produces a percent accuracy and determines whether to flag the post as malicious or not. In the future, if facebook uses this idea we hope they use more data to improve the learning model, which currently has an accuracy rate of about 93.4%. The model uses the status id, message, number of comments, number of shares, likes, loves, reactions, comments and the polarity of the comments as inputs for the model, and focuses on flagging a specific user as opposed to a post at first. Once the user is flagged, the individual posts are checked based on the algorithm and are flagged if appropriate. 

## How we built it
To build this machine learning system, we used the scikit learning library to create a linear regression model for determining the result given specific data. For training the model, we used a web-crawler based on facebook's graph api to aggregate posts between specific dates, and all of the likes and comments and reactions as appropriate. We had over 200 data inputs to feed in the model, and therefore over 1000 data points. We also used BuzzFeed's open source facebook fake or real data for labeling the posts, using this data to train the model as well.

## Challenges we ran into
We ran into a lot of challenges with aggregating the data and actually creating the machine learning algorithm. There were so many errors, and sometimes it worked and other times it just refused. However, with perserverence we were able to debug most of the problems and create a working prototype. However, given more time the web crawler and algorithm for machine learning, in addition to the web app, will be flawless.

## Accomplishments that we're proud of
We are proud that the success rate for the ml algorithm is so high, thanks to the carefully chosen parameters for the model and good data that we collected. By creating the model this carefully, the results that we get are impressive, especially because we chose a linear regression model in scikit-learn, which is optimized for text-based models.

## What we learned
Originally none of us had any experience using machine learning or web crawling, but by the end of these 36 hours, we are confident enough to say we did it. We are not experts by any means in ml or aggregating good data, but our preliminary results are fairly impressive. We also learned to use many apis, including the facebook api and beautiful-soup, both of which are fairly advanced and capable tools for future projects.

## What's next for Fakebook
Fakebook hopes that the technology pioneered today will be implemented in one form or another to combat fake news on a multitude of social networks. Deceiving posts are a large problem in today's society, as people struggle to discern what is real and what has an agenda. Furthermore we acknowledge that what we accomplished this weekend is amazing but it is just one small step in combating a larger issue in social platforms, in preventing hate-speech and promoting healthy discourse. Maybe in the near future Fakebook can work with Facebook or another social network to improve their algorithms for detecting fake news.
