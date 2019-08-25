## Reddit Scrapper

A python script using [PRAW](https://praw.readthedocs.io/en/latest/index.html) that lets you download media files from your favourite subreddits and exports posts info in a .csv format.

## DEMO

![Alt Text](https://media.giphy.com/media/RIeMBlyv06jMJEQgx8/giphy.gif)

## Getting Started

First setup a reddit app from [here](https://www.reddit.com/prefs/apps) <br>

make sure you put http://localhost:8080 in the redirect url field <br>

![alt text](https://i.imgur.com/bVCFHPI.png) <br>

Get your client id, client secret and user agent for auth purposes. <br>

![alt text](https://i.imgur.com/mD5vcma.png) <br>

git clone https://github.com/asjadanis/reddit-scrapper.gitt <br>
pip install -r requirements.txt <br>
<br>

## Usage

python reddit-scrapper.py --client_id 'client-id' --client_secret 'client-secret' --user_agent 'user-agent' --subreddits ProgrammerHumor memes --limit 100 --username 'reddit user name' --password 'reddit password' <br>
python reddit-scrapper.py -h <br>

--username & --password are option <br>
--subreddits list of subreddits to fetch posts from
