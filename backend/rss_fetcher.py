# rss_fetcher.py
import feedparser

RSS_FEED_URL = "https://hnrss.org/newest?q=AI"

def fetch_rss_feed():
    # Parse the RSS feed
    feed = feedparser.parse(RSS_FEED_URL)
    articles = []
    links = []
    for entry in feed.entries:
        link = entry.link
        if link != "https://news.ycombinator.com/newest":
            articles.append({
                'title': entry.title,
                'link': link,
                'summary': entry.summary
            })
            links.append(link)
    return articles, links