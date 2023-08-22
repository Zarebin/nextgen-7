#!/usr/bin/python3
import feedparser
import json

def read_rss_links(file_path):
    with open(file_path, 'r') as file:
        rss_links = [line.strip() for line in file]
    return rss_links

def extract_rss_items(rss_links):
    rss_items = []
    for link in rss_links:
        feed = feedparser.parse(link)
        rss_items.extend(feed.entries)
    return rss_items

def save_to_json(items):
    with open('rss_items.json', 'w') as json_file:
        json.dump(items, json_file, indent=4)

def insert_to_kafka(rss_urls):
    rss_links = read_rss_links(rss_urls)
    rss_items = extract_rss_items(rss_links)
	
	# RSS items extracted and saved to rss_items.json
    save_to_json(rss_items)
	
	# Call your function to add to kafka here
		
