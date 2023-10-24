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
    if output_dir.exists() and not output_dir.is_dir():
        raise FileExistsError(f"Cannot use {output_dir!r} as output directory because it is a file!")
    output_dir.mkdir(exist_ok=True)

    reddit = get_reddit()

    for subreddit_name in tqdm(SUBREDDITS, desc="subreddits", position=1):
        (output_dir / subreddit_name).mkdir(exist_ok=True)
        posts_file_path = output_dir / subreddit_name / "posts.pickle"
        if not posts_file_path.exists():
            # Save posts to file
            recent_posts: List[Submission] = list(reddit.subreddit(subreddit_name).new(limit=1000))
            with posts_file_path.open("wb") as posts_file:
                pickle.dump(recent_posts, posts_file)

        comments_file_path = output_dir / subreddit_name / "comments.pickle"
        if not comments_file_path.exists():
            with posts_file_path.open("rb") as posts_file:
                recent_posts = pickle.load(posts_file)
            recent_posts_comments: List[Comment] = []
            for post in tqdm(recent_posts, desc="posts", leave=False, position=0):
                # This apparently deals with the API equivalent of the "see more" buttons
                post.comments.replace_more(limit=None)
                # This is supposed to visit all comments (not just top level)
                recent_posts_comments.extend(post.comments.list())
            with comments_file_path.open("wb") as comments_file:
                pickle.dump(recent_posts_comments, comments_file)


if __name__ == "__main__":
    main()
