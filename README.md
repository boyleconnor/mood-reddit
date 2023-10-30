# Mood-Reddit

## Set up

You'll need to create a Reddit API "app" and get its credentials in order to run these scripts. While logged into the Reddit account that you want to associate with this app, go to the ["apps" prefs page](https://www.reddit.com/prefs/apps) and create "script"-type app. Then copy the app ID from under the app name and the app secret. Do not share any of these publicly in any form.

In order to make these credentials accessible to the scripts in this repo, you will have to provide them as environment variables or create a [dotenv](https://pypi.org/project/python-dotenv/) file. To use the dotenv file option, create a file in this repo directory named `.env` and fill it with the following content:

```bash
CLIENT_ID="XXXXXXXXXXXXXXXXXXXXXX"
CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
USER_AGENT="ubuntu:com.example.mood_mentions_scraper:v0.0.0 (by u/Reddit-Username-Here)"
```

replacing "xxxxx" with the appropriate values (keep the quotation marks). Also, you should replace "ubuntu" with the name of operating system you are running on and "Reddit-Username-Here" with the Reddit username responsible for authoring this script.

## Run

- `scrape.py` downloads the ~1,000 most recent posts from selected subreddits (saving them with [`pickle`](https://docs.python.org/3/library/pickle.html))
- `check_mentions.py` scans those pickled downloads for mentions of keywords "mood", "hello mood", etc.
