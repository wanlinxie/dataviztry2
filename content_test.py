import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_url_file(filename):
    urls = []
    for url in open(filename):
        if "crunch-report" not in url:
            urls.append(url.rstrip('\n'))

    return parse_all_urls(urls)


def parse_all_urls(urls):
    contents = []
    dates = []
    i = 0
    for url in urls:
        temp = url.split('/')
        date_temp = temp[4]+"/"+temp[5]+"/"+temp[3]
        dates.append(date_temp)
        contents.append(parse_url(url))
        i+=1
        if i % 20 == 0:
            print("Have parsed %d urls" %i)
    return dates, urls,contents


# format : tilte + "\" + content
def parse_url(url):
    # Make the request to a url
    r = requests.get(url)

    # Create soup from content of request
    c = r.content

    soup = BeautifulSoup(c, "lxml")

    # Find the element on the webpage
    main_title = soup.find('h1', attrs={'class': 'article__title'})
    # main_title

    main_content = soup.find('div', attrs={'class': 'article-content'})
    # main_content

    # Init
    title = ""
    content = ""

    # Parse title
    title = main_title.text

    # Extract content
    paragraphs = main_content.find_all('p')

    for p in paragraphs:
        content += (p.text + " ")

    return (title + "\n" + content)

# Parse file
filename = '2013facebook'
dates,urls,contents = parse_url_file(filename + ".txt")

# f = open(filename + "_contents.txt", "w")
# for content in contents:
#   f.write(content + '\n')

import nltk

from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('vader_lexicon')
# sentences = []
articles = contents

sid = SentimentIntensityAnalyzer()
final_data = {}
for i in range(len(articles)):
    sentences = []
    lines_list = tokenize.sent_tokenize(articles[i])
    sentences.extend(lines_list)

    scores = {}
    scores['pos'] = 0
    scores['neg'] = 0
    scores['neu'] = 0
    scores['compound'] = 0



    for sentence in sentences:
        ss = sid.polarity_scores(sentence)

        scores['pos'] += ss['pos']
        scores['neg'] += ss['neg']
        scores['neu'] += ss['neu']
        scores['compound'] += ss['compound']

    for k in sorted(scores):
        scores[k] /= len(sentences)

    print(i, scores)
    final_data['dates'] = final_data.get('dates',[])+[dates[i]]
    final_data['url'] = final_data.get("url",[])+ [urls[i]]
    final_data['scores'] = final_data.get('scores', []) + [scores['compound']]



data = pd.DataFrame.from_dict(final_data)
data.to_csv("2013facebook_final.csv",index=False)






