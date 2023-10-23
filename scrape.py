import argparse
import os
import pickle
from pathlib import Path
from typing import List

import praw
from dotenv import load_dotenv
from praw.models import Submission, Comment
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
        user_agent="linux:com.example.mood_mentions:v0.0.0 (by u/Acrobatic-Hawk9591)",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=Path("./subreddits_data"), type=Path)
    args = parser.parse_args()

    output_dir: Path = args.output_dir
    if output_dir.exists():
        raise FileExistsError(f"Output directory {output_dir!r} already exists!")
    output_dir.mkdir()

    reddit = get_reddit()

    for subreddit_name in tqdm(SUBREDDITS, desc="subreddits", position=0):
        recent_posts: List[Submission] = list(reddit.subreddit(subreddit_name).new(limit=1000))
        (output_dir / subreddit_name).mkdir()

        # Save posts to file
        with (output_dir / subreddit_name / "posts.pickle").open("wb") as posts_file:
            pickle.dump(recent_posts, posts_file)

        recent_posts_comments: List[Comment] = []
        for post in tqdm(recent_posts, desc="posts", leave=False, position=1):
            # This apparently deals with the API equivalent of the "see more" buttons
            post.comments.replace_more(limit=None)
            # This is supposed to visit all comments (not just top level)
            recent_posts_comments.extend(post.comments.list())
        with (output_dir / subreddit_name / "comments.pickle").open("wb") as comments_file:
            pickle.dump(recent_posts_comments, comments_file)


if __name__ == "__main__":
    main()
