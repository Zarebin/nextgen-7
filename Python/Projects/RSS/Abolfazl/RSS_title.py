#!/usr/bin/python3
import feedparser
def extract_title(rss_link):
	try:
		NewsFeed = feedparser.parse(rss_link)
		titles = [entry.title for entry in feed.entries]
		return titles
	except Exception as e:
		print(f"Error: {e}")
		return []

