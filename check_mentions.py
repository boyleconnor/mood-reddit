import argparse
import pickle
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from praw.models import Comment, Submission

from scrape import DEFAULT_DATA_DIR

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

def get_created(post: Submission) -> datetime:
    return datetime.fromtimestamp(post.created)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=DEFAULT_DATA_DIR)
    args = parser.parse_args()

    output_dir: Path = args.output_dir

    records = []
    for subreddit_dir in output_dir.iterdir():
        subreddit = subreddit_dir.name
        comments: List[Comment] = pickle.load((subreddit_dir / 'comments.pickle').open('rb'))
        posts: List[Submission] = pickle.load((subreddit_dir / 'posts.pickle').open('rb'))

        comment_by_id = {comment.id: comment for comment in comments}

        comment_ancestors_by_id: Dict[str, List[Comment]] = {}
        for comment in comments:
            comment_ancestors_by_id[comment.id] = []
            ancestor_id: str = comment.parent_id
            while not ancestor_id.startswith("t3"):
                ancestor = comment_by_id[ancestor_id[3:]]
                comment_ancestors_by_id[comment.id].append(ancestor)
                ancestor_id = ancestor.parent_id

        post_mentions = Counter()
        comment_mentions = Counter()
        replies_to_comment_mentions = Counter()

        for keyword in KEYWORDS:
            # Check that the keyword occurs, but not as part of another word ("\b" = word boundary)
            pattern = re.compile(rf"\b{keyword}\b")
            for post in posts:
                if pattern.search(post.selftext):
                    post_mentions[keyword] += 1
            for comment in comments:
                if pattern.search(comment.body):
                    comment_mentions[keyword] += 1
                if any(pattern.search(ancestor.body) for ancestor in comment_ancestors_by_id[comment.id]):
                    replies_to_comment_mentions[keyword] += 1

        start, end = min(get_created(post) for post in posts), max(get_created(post) for post in posts)
        records.append({
            "subreddit": subreddit, "start": str(start), "end": str(end),
            "post_mentions": dict(post_mentions), "comment_mentions": dict(comment_mentions),
            "replies_to_comment_mentions": dict(replies_to_comment_mentions),
            "total_posts": len(posts), "total_comments": len(comments)
        })

    for record in records:
        print(record)


if __name__ == "__main__":
    main()
