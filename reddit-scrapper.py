import praw
import argparse
import urllib
import os
import pandas as pd
import datetime

class RedditCollector:
  def __init__(self, client_id, client_secret, user_agent, subreddits_list, limit, username, password):

    self.client_id = client_id
    self.client_secret = client_secret
    self.user_agent = user_agent
    self.subreddits_list = subreddits_list
    self.limit = limit
    self.image_urls = []
    self.image_titles = []
    self.image_scores = []
    self.image_timestamps = []
    self.image_ids = []
    self.gif_urls = []
    self.gif_titles = []
    self.gif_scores = []
    self.gif_timestamps = []
    self.gif_ids = []
    self.posts = []
    self.post_titles = []
    self.post_scores = []
    self.post_urls = []
    self.post_ids = []
    self.post_timestamps = []
    self.post_text = []
    self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent, username=username, password=password)
    print 'Reddit User: ', self.reddit.user.me()



  def collect_data(self):
    print 'Fetching data...'
    allowed_image_extensions = ['.jpg', '.jpeg', '.png']
    allowed_gif_extensions = ['.gif']
    for subreddit_name in self.subreddits_list:
      subreddit = self.reddit.subreddit(subreddit_name)
      posts = subreddit.hot(limit=self.limit)
      for post in posts:
        _, ext = os.path.splitext(post.url)
        if ext in allowed_image_extensions:
          self.image_urls.append(post.url.encode('utf-8'))
          self.image_titles.append(post.title.encode('utf-8'))
          self.image_scores.append(post.score)
          self.image_timestamps.append(datetime.datetime.fromtimestamp(post.created))
          self.image_ids.append(post.id)
        if ext in allowed_gif_extensions:
          self.gif_urls.append(post.url)
          self.gif_titles.append(post.title.encode('utf-8'))
          self.gif_scores.append(post.score)
          self.gif_timestamps.append(datetime.datetime.fromtimestamp(post.created))
          self.gif_ids.append(post.id)
        if post.is_self:
          self.post_urls.append(post.url.encode('utf-8'))
          self.post_titles.append(post.title.encode('utf-8'))
          self.post_scores.append(post.score)
          self.post_timestamps.append(datetime.datetime.fromtimestamp(post.created))
          self.post_ids.append(post.id)
          self.post_text.append(post.selftext.encode('utf-8'))
    print 'Data Fetched !!!'

  def save_data(self):
    print 'Writing to disk...'
    
    allowed_image_extensions = ['.jpg', '.jpeg', '.png']
    allowed_gif_extensions = ['.gif', '.gifv']
    
    if len(self.image_ids) > 0:
      if not os.path.exists('./images'):
        os.mkdir('./images')
    
    if len(self.gif_ids) > 0:
      if not os.path.exists('./gifs'):
        os.mkdir('./gifs')
    
    if len(self.post_ids) > 0:
      if not os.path.exists('./posts'):
        os.mkdir('./posts')

    for index, url in enumerate(self.image_urls):
      _, ext = os.path.splitext(url)
      if ext in allowed_image_extensions:
        try:
          print 'downloading ', self.image_urls[index]
          urllib.urlretrieve(self.image_urls[index], './images/' + self.image_titles[index] + ext)
        except:
          print 'something went wrong while downloading ', self.image_urls[index]
    for index, url in enumerate(self.gif_urls):
      _, ext = os.path.splitext(url)
      if ext in allowed_gif_extensions:
        try:
          print 'downloading ', self.gif_urls[index]
          urllib.urlretrieve(self.gif_urls[index], './gifs/' + self.gif_titles[index] + ext)
        except:
          print 'something went wrong while downloading ', self.gif_urls[index]
    print "Done writing data !!!"
  def export_to_csv(self):
    if len(self.image_ids) > 0:
      dataframe = pd.DataFrame({
        'Title': self.image_titles,
        'Score': self.image_scores,
        'Url': self.image_urls,
        'Timestamp': self.image_timestamps,
        'ID': self.image_ids
      })
      csv = dataframe.to_csv(r'./images/images.csv', index=True, header=True)
    
    if len(self.gif_ids) > 0:
      dataframe = pd.DataFrame({
        'Title': self.gif_titles,
        'Score': self.gif_scores,
        'Url': self.gif_urls,
        'Timestamp': self.gif_timestamps,
        'ID': self.gif_ids
      })
      csv = dataframe.to_csv(r'./gifs/gifs.csv', index=True, header=True)

    if len(self.post_ids) > 0:
      dataframe = pd.DataFrame({
        'Title': self.post_titles,
        'Score': self.post_scores,
        'Url': self.post_urls,
        'Timestamp': self.post_timestamps,
        'ID': self.post_ids,
        'Text': self.post_text
      })
      csv = dataframe.to_csv(r'./posts/posts.csv', index=True, header=True)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = 'A script to collect images/gifs from reddit')
  parser.add_argument('--client_id', action='store', dest='client_id', help='your reddit app client id', required=True)
  parser.add_argument('--client_secret', action='store', dest='client_secret', help='your reddit app client secret', required=True)
  parser.add_argument('--user_agent', action='store', dest='user_agent', help='your reddit app user agent', required=True)
  parser.add_argument('--username', action='store', dest='username', help='your reddit username')
  parser.add_argument('--password', action='store', dest='password', help='your reddit password')
  parser.add_argument('--subreddits', action='store', dest='subreddits_list', nargs='+', help='subreddits to collect memes from', required=True)
  parser.add_argument('--limit', action='store', dest='limit', type=int, help='limit to grab posts', required=True)
  args = parser.parse_args()

  data_collector = RedditCollector(client_id=args.client_id, 
                                client_secret=args.client_secret, 
                                user_agent=args.client_secret, 
                                subreddits_list=args.subreddits_list, 
                                limit=args.limit,
                                username=args.username,
                                password=args.password)
  # data_collector.collect_data()
  # data_collector.save_data()
  # data_collector.export_to_csv()
