import os
from collections import Counter
from typing import List

import praw
from dotenv import load_dotenv
from praw.models import Submission
from tqdm import tqdm

load_dotenv()

# FIXME: Incomplete
SUBREDDITS = [
    "Marijuana",
    "trees",
    "420",
    "CannabisExtracts",
    "Delta8"
]

KEYWORDS = [
    "HelloMood",
    "Hellomood",
    "hellomood",
    "Hello Mood",
    "Hello mood",
    "hello mood",
    "Mood",
    "mood"
]


def get_reddit() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT"),
    )


def main():
    reddit = get_reddit()

    matching_posts = Counter()
    matching_comments = Counter()
    # Number of comments for whom any ancestor contains the keyword
    comments_with_matching_ancestors = Counter()

    for subreddit_name in tqdm(SUBREDDITS, desc="subreddits", position=0):
        recent_posts: List[Submission] = list(reddit.subreddit(subreddit_name).new(limit=1000))[:10]
        for post in tqdm(recent_posts, desc="posts", leave=False, position=1):

            # Count totals:
            matching_posts[None] += 1
            for keyword in KEYWORDS:
                if keyword in post.selftext:
                    matching_posts[keyword] += 1
            # This apparently deals with the API equivalent of the "see more" buttons
            post.comments.replace_more(limit=None)
            # This is supposed to visit all comments (not just top level)
            for comment in post.comments.list():

                # Get all ancestors of comment
                ancestors = [comment]
                while ancestors[-1].parent_id.startswith('t1'):
                    ancestors.append(ancestors[-1].parent())

                # Count totals:
                matching_comments[None] += 1
                for keyword in KEYWORDS:
                    if any(keyword in ancestor.body for ancestor in ancestors):
                        comments_with_matching_ancestors[keyword] += 1
                    if keyword in comment.body:
                        matching_comments[keyword] += 1

    print(matching_posts)
    print(matching_comments)
    print(comments_with_matching_ancestors)


if __name__ == "__main__":
    main()
