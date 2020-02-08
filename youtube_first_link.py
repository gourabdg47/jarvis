from bs4 import BeautifulSoup as bs
import requests

import urllib.request

def get_first_link(link):
    content = requests.get(link)
    soup = bs(content.content, "html.parser")

    #soup = bs(urllib.request.urlopen(link))
    title = soup.title.text
    links = []
    
    for a in soup.find_all('a', href=True):
        #print ("Found the URL:", a['href'])
        if '/watch?v=' in a['href']:
            links.append(a['href'])
            #print(links)
        else:
            pass

    return links[0]


# l = 'https://www.youtube.com/results?search_query=Bruno+Fernandes+skills'
# a = get_first_link(l)

# print(a)
