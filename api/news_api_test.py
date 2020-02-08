from newsapi import NewsApiClient
from datetime import datetime

# Init
newsapi = NewsApiClient(api_key = 'a173ce6b6bc748578c3b9de44a026493')

topic = ['bitcoin']
for i, val in enumerate(topic):
    topic = topic[i]

# /v2/top-headlines
top_headlines = newsapi.get_everything(q=topic,
                                        sources='bbc-news,the-verge',
                                        domains='bbc.co.uk,techcrunch.com',
                                        language='en',
                                        page_size = 5)


#print(top_headlines.keys()  )      
articles = top_headlines['articles'] 
print("totalResults: ",top_headlines['totalResults'])

for i, val in enumerate(articles):
    print((i), val['title'])
print('\n')

# for i, val in articles[0].items():
#     print(i.ljust(15), val)

print('\n', datetime.today().strftime('%Y-%m-%d'))