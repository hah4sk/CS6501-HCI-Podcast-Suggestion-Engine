import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentiment:
	def __init__(self):
		self.sid = SentimentIntensityAnalyzer()

	def sentiment(self, s):
		return self.sid.polarity_scores(s)
