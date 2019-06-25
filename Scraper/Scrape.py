import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os


if __name__ == '__main__':
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    url = 'http://theweekinchess.com/twic'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.findAll('a')
    links = []
    for tag in tags:
        if 'PGN' in tag.text:
            link = tag['href']
            if '.zip' in link:
                links.append(link)

    zips = os.listdir(parent + '/zips')
    skip_link = False
    for link in links:
        for zip_file in zips:
            if zip_file in link:
                skip_link = True
        if not skip_link:
            urllib.request.urlretrieve(link, parent + '/zips/' + link[link.find('zips/') + 5:])
            time.sleep(30)

else:
    exit(-1)