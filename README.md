<p float="left">
  <img src="https://github.com/Wazzabeee/scraping_tool/blob/main/src/images/screenshots/search_tab.PNG" width="415" />
  <img src="https://github.com/Wazzabeee/scraping_tool/blob/main/src/images/screenshots/user_tab.PNG" width="415" /> 
</p>

# Twitter Scraping Tool
 
![Python version](https://img.shields.io/badge/Python-3.8-blue)

## About
This program allow the user to retrieve tweets from Twitter's API using the library Tweepy via a GUI or a CRON automatization.

This project was made part of my internship at the "Human Computer Humans Interacting with Computers at University of Primorska" lab (HICUP Lab).

## Setup
To use this program, you will need your API keys retrieved after [creating a developer account at Twitter](https://developer.twitter.com/en/apply-for-access).

Once retrieved the keys must be filled as follows.
[Keys format](img/credentials.png)

**How to use**
---
```bash
# Clone this repository
$ git clone https://github.com/scraping_tool

# Go into the repository
$ cd scraping_tool

# Install requirements
$ pip3 install -r requirements.txt

# Fill credentials in credentials.py
# See "Setup"

# Run the app
$ python main.py
```

