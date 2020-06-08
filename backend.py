#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import re
from bottle import *
from subprocess import Popen, PIPE, STDOUT


SEARCH_SIMILARITY_THRESHOLD = .4

HEADERS = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')}

def search_meme(text):
    r = requests.get('http://knowyourmeme.com/search?q=%s' % text, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    memes_list = soup.find(class_='entry_list')
    if memes_list:
        meme_path = memes_list.find('a', href=True)['href']
        return meme_path.replace('-', ' '), 'https://knowyourmeme.com%s' % meme_path
    return None, None

def about(text):
    meme_name, url = search_meme(text)
    if meme_name and SequenceMatcher(None, text, meme_name).ratio() >= SEARCH_SIMILARITY_THRESHOLD:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        entry = soup.find('h2', {'id': 'about'})
        return '%s. %s' % (meme_name.split('/')[-1].title(), entry.next.next.next.text)

def origin(text):
    meme_name, url = search_meme(text)
    if meme_name and SequenceMatcher(None, text, meme_name).ratio() >= SEARCH_SIMILARITY_THRESHOLD:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        entry = soup.find('h2', {'id': 'origin'})
        return '%s. %s' % (meme_name.split('/')[-1].title(), entry.next.next.next.text)

def spread(text):
    meme_name, url = search_meme(text)
    if meme_name and SequenceMatcher(None, text, meme_name).ratio() >= SEARCH_SIMILARITY_THRESHOLD:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        entry = soup.find('h2', {'id': 'spread'})
        return '%s. %s' % (meme_name.split('/')[-1].title(), entry.next.next.next.text)

def image(text):
    meme_name, url = search_meme(text)
    if meme_name and SequenceMatcher(None, text, meme_name).ratio() >= SEARCH_SIMILARITY_THRESHOLD:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        entry = soup.find('meta', property='og:image')["content"]
        return str(entry)

@get("/<meme>")
def index(meme):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "text/plain"
    x = about(meme) + "<br><h2>Origin</h2><p style=\"text-align:left;\">" + re.sub(r"\[(.*?)\]", "", origin(meme)) + "</p><br><h2>Spread</h2><p style=\"text-align:left;\">" + re.sub(r"\[(.*?)\]", "", spread(meme)) + "</p>{{img}}" + image(meme)
    return x

run(ip="127.0.0.1", port=8039, server="tornado")