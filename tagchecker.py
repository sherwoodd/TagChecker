import numpy as np
import pandas as pd
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os

RELOADS = 4

def simple_get(url):
    """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
        Returns True if the response seems to be HTML, False otherwise.
        """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
    print(e)

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def getURLs():
    file = os.listdir('input')[0]
    df = pd.read_excel('input/'+file, header=None)
    metadata = {}
    for i in range(1,5):
        metadata[df.loc[i,0]]=df.loc[i,7]
    urls = []
    for i in range(11,len(df)):
        cell = df.loc[i,13]
        temp = cell.split('\n')[1]
        urls.append(temp.replace('ad/','adi/'))
    
    return(metadata, urls)

metadata, urls = getURLs()
folder = 'output/' + metadata['Campaign Name']
if not os.path.exists(folder):
    os.makedirs(folder)

for x in range(len(urls)):
    filename = folder+'/ad'+str(x+1)+'.txt'
    print("This is " + urls[x], file=open(filename,"w"))
    print('\n',file=open(filename,"a"))

    for r in range(RELOADS):
        print('\n',file=open(filename,"a"))
        print('######################### REFRESH PAGE #########################', file=open(filename,"a"))
        print('\n',file=open(filename,"a"))
        raw_html = simple_get(urls[x])
        html = BeautifulSoup(raw_html, 'html.parser')
        script = html.select('script')[1].text
        for i in script.split('ClickTag'):
            if i[0].isdigit():
                url = i.split("destinationUrl:")[1].split("'")[1]
                name = url.split('utm_term\\')[-1].split('\\')[0].replace('%20',' ').replace('x3d','')
                print('Name: '+ name, file=open(filename, "a"))
                print('Full URL: ' + url, file=open(filename, "a"))
                print(file=open(filename, "a"))


