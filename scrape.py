import praw
from praw.models import MoreComments
from psaw import PushshiftAPI
import pandas as pd
import numpy as np
import re
from tqdm import tqdm

from password_utils import praw_keys
from sentiment import Sentiment

class PPAW:
	def __init__(self):
		self._psaw()
		self.s = Sentiment()

	def _psaw(self):
		config = dict(zip(['client_id', 'client_secret', 'user_agent'], praw_keys()))
		self.r = praw.Reddit(**config)
		self.ps = PushshiftAPI(self.r)

	def get_posts(self):
		raw_pl = self.ps.search_submissions(q='Weekly podcast post', subreddit='Podcasts', limit=1000)
		self.pl = [post for post in list(raw_pl) if re.match(r"^Weekly podcast post", post.title)]
		return self.pl

	def _get_tlcs(self, id):
		s = self.r.submission(id=id)
		s.comments.replace_more(limit=0)
		return s.comments

	#TODO: Abstract replacement pairs into iterable or method
	#Text extraction is unfortunately an imprecise science. 
	def _extract_tlc(self, tlc):
		#Upvotes
		upv = tlc.score
		identifier = tlc.id

		#Upvote > 0 to protect against self-advertisement and save my processor
		if upv > 0:  
			#Tags: Willfully ignoring people who use (), tell them to get it together
			#Title: Ignoring episode numbers, raw title info
			body = tlc.body

			#Get matches
			rx = r"\A[\s\*\\\_]*(?P<tags>(?:\[.+?\]\s*)*)(?P<title>.*?)\s*?(?:\||Ep(?:isode)??)"
			re.compile(rx)
			match = re.search(rx, body)

			#Clean tags
			tags = match.group("tags")
			tags = tags.replace('[', '').replace(']', '').replace('\\', '').replace('\n', ' ').replace('*', '').replace('(', '').replace('\"', '').replace(')', '')
			tags = tags.replace(',', '/').replace(' - ', '/').replace('&', '/').replace('+', '/').replace(';', '/')
			tags = tags.split('/')
			tags = list(map(lambda x: x.strip().lower(), tags))

			#Clean titles
			title = match.group("title")
			title = re.sub("[\(\[].*?[\)\]]", "", title)
			title = re.sub("(?:\W*)\b", "", title)
			title = title.replace('*', '').replace('\\', '').replace('-', '').replace('[', '').replace('/', '').strip().lower()
			title = title.encode('ascii', errors='ignore').decode() #no unicode

			#Sentiment
			senti = self.s.sentiment(body)
			score = 0
			if senti['neg'] < -0.25 or senti['pos'] > 0.25:
				score = senti['neg'] if abs(senti['neg']) > senti['pos'] else senti['pos']
			return upv, identifier, tags, title, score

	def _proc_sub(self, sub):
		sub_id = sub.id
		df = pd.DataFrame(columns=['Comment_ID', 'Sub_ID', 'Upvotes', 'Sentiment', 'Tags', 'Title'])
		for item in self._get_tlcs(sub_id):
			try:
				upv, identifier, tags, title, score = self._extract_tlc(item)
				if not upv or not identifier or not tags or not title:
					continue
				df = df.append({'Comment_ID':identifier, 'Sub_ID':sub_id, 'Upvotes':upv, 'Sentiment':score, 'Tags':tags, 'Title':title}, ignore_index=True)
			except:
				pass
		return df.explode('Tags')

	def proc_posts(self, posts):
		df = pd.DataFrame(columns=['Comment_ID', 'Sub_ID', 'Upvotes', 'Sentiment', 'Tags', 'Title'])

		post_bar = tqdm(posts)
		for sub in post_bar:
			post_bar.set_description("[scrape] Processing {}".format(sub))
			subdf = self._proc_sub(sub)
			df = df.append(subdf, ignore_index=True)
		df['Tags'].replace('', np.nan, inplace=True)
		df['Title'].replace(['', ':', ')', '.', ',', '\|', '\"'], np.nan, inplace=True)
		df = df.dropna(axis=0, how='any')
		return df