import argparse
import os

import praw
from dotenv import load_dotenv
from praw import Reddit
from praw.models import Submission, Comment

load_dotenv()


def monitor_comments(reddit: Reddit, subreddit_name: str):
    comment: Comment
    for comment in reddit.subreddit(subreddit_name).stream.comments():
        print(f"COMMENT: {comment.body[:100]!r}")


def monitor_submissions(reddit: Reddit, subreddit_name):
    submission: Submission
    for submission in reddit.subreddit(subreddit_name).stream.submissions():
        print(f"SUBMISSION: {submission.selftext[:100]!r}")


def main():
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("subreddit", type=str)
    parser.add_argument("--monitor", type=str, choices=["comments", "submissions"], required=True)
    args = parser.parse_args()

    if args.monitor == "comments":
        monitor_comments(reddit, args.subreddit)
    elif args.monitor == "submissions":
        monitor_submissions(reddit, args.subreddit)


if __name__ == "__main__":
    main()
