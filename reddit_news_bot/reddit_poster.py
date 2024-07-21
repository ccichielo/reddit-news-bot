import praw

class RedditPoster:
    def __init__(self, client_id, client_secret, username, password, subreddit_name):
        try:
            reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent='eq2-bot:v0.0.1 (by /u/kythosmeltdown)',
                    username=username,
                    password=password
            )
            self.__subreddit = reddit.subreddit(subreddit_name)
        except Exception as e:
            print(f"Exception thrown during Reddit client initialization: {e}")
            raise

    def submit(self, title, content, flair_id):
        try:
            if not content:
                raise ValueError("Content cannot be empty")
            submission = self.__subreddit.submit(title, selftext=content)
            submission.flair.select(flair_id)
            print(f"Post submitted: {submission.url}")
        except Exception as e:
            print(f"Exception thrown submitting post: {e}")
            raise

