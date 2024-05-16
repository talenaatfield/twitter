import feedparser
import requests
import time
import html
from datetime import datetime
from bs4 import BeautifulSoup

rssfeedurls = ["https://nitter.poast.org/notlieu/rss"] # your rss feeds urls here, replace notlieu with any other twitter user
webhookURL = "DISCORD_WEBHOOK_HERE" # your discord webhook here
entriesfile = "entries.txt"


def send2discord(embed):
    payload = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}
    requests.post(webhookURL, json=payload, headers=headers)


def parse_rss_feeds():
    newentries = False
    for RSS_FEED_URL in rssfeedurls:
        feed = feedparser.parse(RSS_FEED_URL)
        for entry in feed.entries:
            entryid = f"{RSS_FEED_URL}:{entry.id}"
            if entryid not in sententries:
                title = entry.title
                creator = entry.author
                description = entry.description
                link = entry.link
                pubdate = entry.published
                soup = BeautifulSoup(description, "html.parser")
                image_url = soup.find("img")["src"] if soup.find("img") else None

                embed = {
                    "title": title,
                    "url": link,
                    "author": {"name": creator},
                    "fields": [
                        {"name": "Author", "value": creator},
                        {"name": "Time", "value": pubdate},
                        {"name": "Description", "value": description},
                    ],
                    "image": {"url": image_url},
                }

                send2discord(embed)
                sententries.add(entryid)
                newentries = True

    return newentries


try:
    with open(entriesfile, "r") as f:
        sententries = set(line.strip() for line in f)
except FileNotFoundError:
    sententries = set()

while True:
    newentries = parse_rss_feeds()
    if not newentries:
        print(f"{datetime.now()} - nothing new")
    with open(entriesfile, "w") as f:
        for entryid in sententries:
            f.write(entryid + "\n")

    time.sleep(60)
