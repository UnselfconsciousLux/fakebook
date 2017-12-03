# fakebook
This is a machine learning app to help identify spam facebook posts and report them to facebook

YHACKS project
Designed to flag potential fake comments based on repeat offending accounts and other indicators for the said account.

## Inspiration
In the current political climate and the widespread issue of fake news on social media, we found it imperative for this problem to be solved. There needs to be quick, reliable flagging of potentially malicious posts that try to deceive other social-media users. By flagging the posts early using machine learning without the input of other users, as is the current system on Facebook, the algorithm produces faster results. This was the inspirational idea for us to pursue the fake news challenge.

## What it does
Fakebook uses advanced linear-regression machine learning algorithms to directly flag users and posts that are used to spread deceiving information. The process used in the demo is relatively simple, in that we upload a facebook user account to a custom web app, and the web app pushes the data crawled from the account using the facebook api to the machine learning algorithm. This algorithm in turn produces a percent accuracy and determines whether to flag the post as malicious or not. In the future, if facebook uses this idea we hope they use more data to improve the learning model, which currently has an accuracy rate of about 93.4%. The model uses the status id, message, number of comments, number of shares, likes, loves, reactions, comments and the polarity of the comments as inputs for the model, and focuses on flagging a specific user as opposed to a post at first. Once the user is flagged, the individual posts are checked based on the algorithm and are flagged if appropriate. 

## How we built it
To build this machine learning system, we used the scikit learning library to create a linear regression model for determining the result given specific data. For training the model, we used a web-crawler based on facebook's graph api to aggregate posts between specific dates, and all of the likes and comments and reactions as appropriate. We had over 200 data inputs to feed in the model, and therefore over 1000 data points. We also used BuzzFeed's open source facebook fake or real data for labeling the posts, using this data to train the model as well.

## Challenges we ran into
We ran into a lot of challenges with aggregating the data and actually creating the machine learning algorithm. There were so many errors, and sometimes it worked and other times it just refused. However, with perserverence we were able to debug most of the problems and create a working prototype. However, given more time the web crawler and algorithm for machine learning, in addition to the web app, will be flawless.

## Accomplishments that we're proud of

## What we learned

## What's next for Fakebook
