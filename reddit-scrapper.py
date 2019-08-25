import praw
import argparse
import urllib
import os
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests

class RedditCollector:
  def __init__(self, client_id, client_secret, user_agent, subreddits_list, limit, username, password):
    
    self.client_id = client_id
    self.client_secret = client_secret
    self.user_agent = user_agent
    self.subreddits_list = subreddits_list
    self.limit = limit
    self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent, username=username, password=password)
    print '>>> Reddit User: ', self.reddit.user.me()



  def collect_data(self):
    print '>>> Fetching data... \n\n'
    allowed_image_extensions = ['.jpg', '.jpeg', '.png']
    allowed_gif_extensions = ['.gif']
    for subreddit_name in self.subreddits_list:
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
      
      self.other_urls = []
      self.other_titles = []
      self.other_scores = []
      self.other_timestamps = []
      self.other_ids = []
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
        else:
          self.other_urls.append(post.url.encode('utf-8'))
          self.other_titles.append(post.title.encode('utf-8'))
          self.other_scores.append(post.score)
          self.other_timestamps.append(datetime.datetime.fromtimestamp(post.created))
          self.other_ids.append(post.id)

      self.save_data(subreddit=subreddit_name)  

  def save_data(self, subreddit):
    print '>>> Writing ', subreddit, ' data to disk... \n\n'

    dirpath = os.path.join('./', subreddit)
    if not os.path.exists(dirpath):
      os.mkdir(dirpath)

    allowed_image_extensions = ['.jpg', '.jpeg', '.png']
    allowed_gif_extensions = ['.gif', '.gifv']
    
    if len(self.image_ids) > 0:
      images_path = os.path.join(dirpath, 'images/')
      if not os.path.exists(images_path):
        os.mkdir(images_path)
    
    if len(self.gif_ids) > 0:
      gifs_path = os.path.join(dirpath, 'gifs/')
      if not os.path.exists(gifs_path):
        os.mkdir(gifs_path)
    
    if len(self.post_ids) > 0:
      posts_path = os.path.join(dirpath, 'posts/')
      if not os.path.exists(posts_path):
        os.mkdir(posts_path)
    
    if len(self.other_ids) > 0:
      others_path = os.path.join(dirpath, 'others/')
      if not os.path.exists(others_path):
        os.mkdir(others_path)

    for index, url in enumerate(self.image_urls):
      _, ext = os.path.splitext(url)
      if ext in allowed_image_extensions:
        try:
          print '>>> downloading ', self.image_urls[index], ' in ', images_path + self.image_titles[index] + ext
          urllib.urlretrieve(self.image_urls[index], images_path + self.image_titles[index] + ext)
        except:
          print '>>> something went wrong while downloading ', self.image_urls[index]
    for index, url in enumerate(self.gif_urls):
      _, ext = os.path.splitext(url)
      if ext in allowed_gif_extensions:
        try:
          print '>>> downloading ', self.gif_urls[index], ' in ', gifs_path + self.gif_titles[index] + ext
          urllib.urlretrieve(self.gif_urls[index], gifs_path + self.gif_titles[index] + ext)
        except:
          print '>>> something went wrong while downloading ', self.gif_urls[index]
    for index, url in enumerate(self.other_urls):
      try:
        print '>>> downloading ', self.other_urls[index], ' in ', others_path + self.other_titles[index]
        if 'gfycat' in self.other_urls[index]:
          self.other_urls[index] = self.other_urls[index] + '.gif'
          page = requests.get(self.other_urls[index])
          soup = BeautifulSoup(page.content, 'html.parser')
          if soup.find('source', attrs={'id': 'mp4Source'}) is not None:
            gif_source = soup.find('source', attrs={'id': 'mp4Source'})['src']
            urllib.urlretrieve(gif_source , others_path + self.other_titles[index] + '.mp4')
      except:
        print '>>> something went wrong while downloading ', self.other_urls[index]
    self.export_to_csv(dirpath=dirpath)
    print "\n>>> Done writing data !!! \n\n"


  def export_to_csv(self, dirpath):
    if len(self.image_ids) > 0:
      images_path = os.path.join(dirpath, 'images', 'images.csv')
      dataframe = pd.DataFrame({
        'Title': self.image_titles,
        'Score': self.image_scores,
        'Url': self.image_urls,
        'Timestamp': self.image_timestamps,
        'ID': self.image_ids
      })
      csv = dataframe.to_csv(images_path, index=True, header=True)
    
    if len(self.gif_ids) > 0:
      gifs_path = os.path.join(dirpath, 'gifs', 'gifs.csv')
      dataframe = pd.DataFrame({
        'Title': self.gif_titles,
        'Score': self.gif_scores,
        'Url': self.gif_urls,
        'Timestamp': self.gif_timestamps,
        'ID': self.gif_ids
      })
      csv = dataframe.to_csv(gifs_path, index=True, header=True)

    if len(self.post_ids) > 0:
      posts_path = os.path.join(dirpath, 'posts', 'posts.csv')
      dataframe = pd.DataFrame({
        'Title': self.post_titles,
        'Score': self.post_scores,
        'Url': self.post_urls,
        'Timestamp': self.post_timestamps,
        'ID': self.post_ids,
        'Text': self.post_text
      })
      csv = dataframe.to_csv(posts_path, index=True, header=True)

    if len(self.other_ids) > 0:
      others_path = os.path.join(dirpath, 'others', 'others.csv')
      dataframe = pd.DataFrame({
        'Title': self.other_titles,
        'Score': self.other_scores,
        'Url': self.other_urls,
        'Timestamp': self.other_timestamps,
        'ID': self.other_ids,
      })
      csv = dataframe.to_csv(others_path, index=True, header=True)

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
  data_collector.collect_data()
