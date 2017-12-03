import json
import datetime
import csv
import time
from textblob import TextBlob
import nltk

nltk.download('punkt')

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
app_id = "377742929333901"
app_secret = "922375a7e0cd8aa306b214de0c1d2223"  # DO NOT SHARE WITH ANYONE!
page_id = file_id = ["184096565021911", "146422995398181", "219367258105115", \
                     "135665053303678", "440106476051475", "346937065399354", "62317591679", \
                     "389658314427637", "114517875225866"]
name_news = ["ABC News Politics", "Addicting Info", "CNN Politics", "Eagle Rising",\
             "Freedom Daily", "Occupy Democrats", "Politico", "Right Wing News", "The Other 98%"]

# input date formatted as YYYY-MM-DD
since_date = "2017-09-19", 
until_date = "2017-09-27", 

access_token = app_id + "|" + app_secret


def request_until_succeed(url):
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()

# Needed to write tricky unicode correctly to csv
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')


def getFacebookCommentFeedUrl(base_url):

    # Construct the URL string
    fields = "&fields=id,message,reactions.limit(0).summary(true)" + \
        ",created_time,comments,from,attachment"
    url = base_url + fields
    return url

def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=message,link,created_time,type,name,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true)"

    return base_url + fields

def getReactionsForStatuses(base_url):

    reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
    reactions_dict = {}   # dict of {status_id: tuple<6>}

    for reaction_type in reaction_types:
        fields = "&fields=reactions.type({}).limit(0).summary(total_count)".format(
            reaction_type.upper())

        url = base_url + fields

        data = json.loads(request_until_succeed(url))['data']

        data_processed = set()  # set() removes rare duplicates in statuses
        for status in data:
            id = status['id']
            count = status['reactions']['summary']['total_count']
            data_processed.add((id, count))

        for id, count in data_processed:
            if id in reactions_dict:
                reactions_dict[id] = reactions_dict[id] + (count,)
            else:
                reactions_dict[id] = (count,)

    return reactions_dict


def processFacebookPageFeedStatus(status):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_type = status['type']

    status_message = '' if 'message' not in status else \
        unicode_decode(status['message'])
    link_name = '' if 'name' not in status else \
        unicode_decode(status['name'])
    status_link = '' if 'link' not in status else \
        unicode_decode(status['link'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(
        status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
        datetime.timedelta(hours=-5)  # EST
    status_published = status_published.strftime(
        '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
        status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
        status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else status['shares']['count']

    return (status_id, status_message, link_name, status_type, status_link,
            status_published, num_reactions, num_comments, num_shares)


def scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date, rows):
    num_processed = 0
    has_next_page = True
    scrape_starttime = datetime.datetime.now()
    after = ''
    base = "https://graph.facebook.com/v2.11"
    node = "/{}/posts".format(page_id)
    parameters = "/?limit={}&access_token={}".format(100, access_token)
    since = "&since={}".format(since_date) if since_date \
        is not '' else ''
    until = "&until={}".format(until_date) if until_date \
        is not '' else ''

    print("Scraping {} Facebook Page: {}\n".format(page_id, scrape_starttime))

    while has_next_page:
        after = '' if after is '' else "&after={}".format(after)
        base_url = base + node + parameters + after + since + until

        url = getFacebookPageFeedUrl(base_url)
        statuses = json.loads(request_until_succeed(url))
        reactions = getReactionsForStatuses(base_url)

        for status in statuses['data']:

            # Ensure it is a status with the expected metadata
            if 'reactions' in status:
                status_data = processFacebookPageFeedStatus(status)
                reactions_data = reactions[status_data[0]]

                # calculate thankful/pride through algebra
                num_special = status_data[6] - sum(reactions_data)
                rows += [status_data + reactions_data + (num_special,)]

            num_processed += 1

        # if there is no next page, we're done.
        if 'paging' in statuses:
            after = statuses['paging']['cursors']['after']
        else:
            has_next_page = False

    print("\nDone!\n{} Statuses Processed in {}".format(
              num_processed, datetime.datetime.now() - scrape_starttime))

def scrapeFacebookPageFeedComments(page_id, access_token, result):

    num_processed_comments = 0
    scrape_starttime = datetime.datetime.now()
    after = ''
    base = "https://graph.facebook.com/v2.11"
    parameters = "/?limit={}&access_token={}".format(
            100, access_token)
    print("Scraping {} Comments From Posts: {}\n".format(
        file_id, scrape_starttime))

    with open('{}_facebook_statuses.csv'.format(file_id), 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # Uncomment below line to scrape comments for a specific status_id
        # reader = [dict(status_id='5550296508_10154352768246509')]

        for status in reader:
            has_next_page = True
                
            while has_next_page:
                node = "/{}/comments".format(status['status_id'])
                after = '' if after is '' else "&after={}".format(after)
                base_url = base + node + parameters + after

                url = getFacebookCommentFeedUrl(base_url)
                # print(url)
                comments = json.loads(request_until_succeed(url))
                #print("\n\n\n\n\n")
                #happens 9 times
                messages = ""
                for comment in comments['data']:
                    #ONE
                    messages += str(str(comment['message']).encode('unicode-escape'))
                    
                    # calculate thankful/pride through algebra
                    #print(str(comment_data).encode('unicode-escape'))
                    if 'comments' in comment:
                        has_next_subpage = True
                        sub_after = ''

                        while has_next_subpage:
                            sub_node = "/{}/comments".format(comment['id'])
                            sub_after = '' if sub_after is '' else "&after={}".format(
                                sub_after)
                            sub_base_url = base + sub_node + parameters + sub_after
                            
                            sub_url = getFacebookCommentFeedUrl(
                                sub_base_url)
                            sub_comments = json.loads(
                                request_until_succeed(sub_url))
                            
                            for sub_comment in sub_comments['data']:
                                #TWO
                                messages += str(str(comment['message']).encode('unicode-escape'))

                                #print((str(sub_comment_data).encode('unicode-escape')))
                                    
                                num_processed_comments += 1
                                if num_processed_comments % 100 == 0:
                                    print("{} Comments Processed: {}".format(
                                        num_processed_comments,
                                        datetime.datetime.now()))
                                    
                            if 'paging' in sub_comments:
                                if 'next' in sub_comments['paging']:
                                    sub_after = sub_comments[
                                        'paging']['cursors']['after']
                                else:
                                    has_next_subpage = False
                            else:
                                has_next_subpage = False

                    # output progress occasionally to make sure code is not
                    # stalling
                    num_processed_comments += 1

                blob = TextBlob(messages)
                polarity_sum = 0
                count = 0
                for sentence in blob.sentences:
                    polarity_sum += sentence.sentiment.polarity
                    count += 1
                avg_polarity = polarity_sum / count
                #print(avg_polarity)
                result += [(avg_polarity,)]
                if 'paging' in comments:
                    if 'next' in comments['paging']:
                        after = comments['paging']['cursors']['after']
                    else:
                            has_next_page = False
                else:
                    has_next_page = False

    print("\nDone!\n{} Comments Processed in {}".format(
        num_processed_comments, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    for i in range(len(page_id)):
        result = []
        rows = []
        with open('{}_data.csv'.format(name_news[i]), 'w') as file:
            w = csv.writer(file)
            w.writerow(["status_id", "status_message", "link_name", "status_type",
                        "status_link", "status_published", "num_reactions",
                        "num_comments", "num_shares", "num_likes", "num_loves",
                        "num_wows", "num_hahas", "num_sads", "num_angrys",
                        "num_special", "polarity_comments"])
            scrapeFacebookPageFeedStatus(page_id[i], access_token, since_date, until_date, rows)
            scrapeFacebookPageFeedComments(file_id[i], access_token, result)
            for j in range(len(rows)):
                w.writerow((rows[j] + result[j]))

# The CSV can be opened in all major statistical programs. Have fun! :)
