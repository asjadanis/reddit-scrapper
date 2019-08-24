import praw
import argparse
import urllib
import os
import pandas as pd
import datetime

class MemeCollector:
  def __init__(self, client_id, client_secret, user_agent, subreddits_list, limit, username, password):
    self.client_id = client_id
    self.client_secret = client_secret
    self.user_agent = user_agent
    self.subreddits_list = subreddits_list
    self.limit = limit
    self.meme_urls = []
    self.meme_titles = []
    self.meme_scores = []
    self.meme_timestamps = []
    self.meme_ids = []
    self.gif_urls = []
    self.gif_titles = []
    self.gif_scores = []
    self.gif_timestamps = []
    self.gif_ids = []
    self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent, username=username, password=password)
    print 'Reddit User: ', self.reddit.user.me()
  def collect_memes(self):
    print 'Fetching memes...'
    allowed_image_extensions = ['.jpg', '.jpeg', '.png']
    allowed_gif_extensions = ['.gif']
    for subreddit_name in self.subreddits_list:
      subreddit = self.reddit.subreddit(subreddit_name)
      posts = subreddit.hot(limit=self.limit)
      for post in posts:
        _, ext = os.path.splitext(post.url)
        if ext in allowed_image_extensions:
          self.meme_urls.append(post.url.encode('utf-8'))
          self.meme_titles.append(post.title.encode('utf-8'))
          self.meme_scores.append(post.score)
          self.meme_timestamps.append(datetime.datetime.fromtimestamp(post.created))
          self.meme_ids.append(post.id)
        if ext in allowed_gif_extensions:
          self.gif_urls.append(post.url)
          self.gif_titles.append(post.title.encode('utf-8'))
          self.gif_scores.append(post.score)
          self.gif_timestamps.append(datetime.datetime.fromtimestamp(post.created))
          self.gif_ids.append(post.id)
    print 'Memes Fetched !!!'

  def save_memes(self):
    print 'Writing Memes to disk...'
    allowed_image_extensions = ['.jpg', '.jpeg', '.png']
    allowed_gif_extensions = ['.gif', '.gifv']
    for index, url in enumerate(self.meme_urls):
      _, ext = os.path.splitext(url)
      if ext in allowed_image_extensions:
        try:
          urllib.urlretrieve(self.meme_urls[index], './memes/' + self.meme_titles[index] + ext)
        except:
          print 'something went wrong while downloading ', self.meme_urls[index]
    print 'Done writing memes !!!'
    print 'Writing gifs to disk...'
    for index, url in enumerate(self.gif_urls):
      _, ext = os.path.splitext(url)
      if ext in allowed_gif_extensions:
        try:
          urllib.urlretrieve(self.gif_urls[index], './gifs/' + self.gif_titles[index] + ext)
        except:
          print 'something went wrong while downloading ', self.gif_urls[index]

  def export_to_csv(self):
    dataframe = pd.DataFrame({
      'Title': self.meme_titles,
      'Score': self.meme_scores,
      'Url': self.meme_urls,
      'Timestamp': self.meme_timestamps,
      'ID': self.meme_ids
    })
    csv = dataframe.to_csv(r'./memes/memes.csv', index=True, header=True)
    dataframe = pd.DataFrame({
      'Title': self.gif_titles,
      'Score': self.gif_scores,
      'Url': self.gif_urls,
      'Timestamp': self.gif_timestamps,
      'ID': self.gif_ids
    })
    csv = dataframe.to_csv(r'./gifs/gifs.csv', index=True, header=True)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = 'A script to collect memes from reddit')
  parser.add_argument('--client_id', action='store', dest='client_id', help='your reddit app client id', required=True)
  parser.add_argument('--client_secret', action='store', dest='client_secret', help='your reddit app client secret', required=True)
  parser.add_argument('--user_agent', action='store', dest='user_agent', help='your reddit app user agent', required=True)
  parser.add_argument('--username', action='store', dest='username', help='your reddit username')
  parser.add_argument('--password', action='store', dest='password', help='your reddit password')
  parser.add_argument('--subreddits', action='store', dest='subreddits_list', nargs='+', help='subreddits to collect memes from', required=True)
  parser.add_argument('--limit', action='store', dest='limit', type=int, help='limit to grab posts', required=True)
  args = parser.parse_args()

  if not os.path.exists('./memes'):
    os.mkdir('./memes')
  if not os.path.exists('./gifs'):
    os.mkdir('./gifs')

  meme_collector = MemeCollector(client_id=args.client_id, 
                                client_secret=args.client_secret, 
                                user_agent=args.client_secret, 
                                subreddits_list=args.subreddits_list, 
                                limit=args.limit,
                                username=args.username,
                                password=args.password)
  meme_collector.collect_memes()
  meme_collector.save_memes()
  meme_collector.export_to_csv()
