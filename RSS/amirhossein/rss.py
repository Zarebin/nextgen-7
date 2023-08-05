from bs4 import BeautifulSoup as bs4
import requests
import feedparser
import urllib.parse
import pandas as pd
import csv


# data
links = {'farsenews': ['https://www.farsnews.ir/'],
        'hamshahrionline': ['https://www.hamshahrionline.ir/']}


def findfeed(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw, 'html.parser')
    feed_urls = html.findAll("link", rel="alternate")
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get("type",None)
            if t:
                if "rss" in t or "xml" in t:
                    href = f.get("href",None)
                    if href:
                        possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site)
    base = parsed_url.scheme+"://"+parsed_url.hostname
    atags = html.findAll("a")
    for a in atags:
        href = a.get("href",None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                possible_feeds.append(base+href)
                possible_feeds.append(href)

    possible_feeds.append(site + 'rss')

    for url in list(set(possible_feeds)):
        print(url)
        f = feedparser.parse(url)
        if len(f.entries) > 0:
            if url not in result:
                result.append(url)

    
    return(set(result))



def save(name, link):
    feed = feedparser.parse(link)

    with open(f'{name}_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fields = ['id', 'title', 'link', 'published', 'summary']
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for entry in feed.entries:
            writer.writerow({'id': entry.id, 'title': entry.title, 'link': entry.link, 'published': entry.published, 'summary': entry.summary})

def update(name, rss_link):
    feed = feedparser.parse(rss_link)

    df = pd.read_csv(f'{name}_data.csv')

    for entry in feed.entries:
        if not entry.id in set(df.id):
            with open(f'{name}_data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
                fields = ['id', 'title', 'link', 'published', 'summary']
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writerow({'id': entry.id, 'title': entry.title, 'link': entry.link, 'published': entry.published, 'summary': entry.summary})

            print(f'{name}_data.csv data_updated')

    # df.to_csv(f'{name}_data.csv')
    print('update finished completely')



def fetch_data():
    for link in links:
        rss_feed = findfeed(links[link][0])
        rss_link = next(iter(rss_feed))
        links[link].append(rss_link)
        save(link, rss_link)


def update_data():
    for link in links:
        update(link, links[link][1])
