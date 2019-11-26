import pandas as pd
import numpy as np
from tqdm import tqdm
from fuzzywuzzy import fuzz, process

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def fuzzy_categories(df, thresh):
	counts = df['Tags'].value_counts()
	t_counts = counts[counts >= thresh].index.tolist()
	tqdm.pandas(desc = '[fuzz] Fuzzing categories')
	df['Fuzzy_Tag'] = df.progress_apply(lambda row: _fuzzy_match(t_counts, row['Tags']), axis=1)
	return df

#TODO: Is there a better title list somewhere? I sure can't find one
def fuzzy_titles(df, thresh):
	counts = df['Title'].value_counts()
	t_counts = counts[counts >= thresh].index.tolist()
	tqdm.pandas(desc = '[fuzz] Fuzzing titles')
	df['Fuzzy_Title'] = df.progress_apply(lambda row: _fuzzy_match(t_counts, row['Title']), axis=1)
	return df

def fuzz_ratio(fuzz):
	ftit = fuzz.apply(lambda row: row['Fuzzy_Title'] == row['Title'], axis = 1).value_counts()
	print('[fuzz] Title fuzz ratio: {0:.4f}'.format(ftit[False]/(ftit[False]+ftit[True])))
	fcat = fuzz.apply(lambda row: row['Fuzzy_Tag'] == row['Tags'], axis = 1).value_counts()
	print('[fuzz] Category fuzz ratio: {0:.4f}'.format(fcat[False]/(fcat[False]+fcat[True])))

def _fuzzy_match(counts, query):
	suggestion = process.extractOne(query, counts, scorer=fuzz.token_set_ratio)
	#Differential threshold: more likely names are allowed more leeway
	return suggestion[0] if (suggestion[1] > 80) or (suggestion[1] > 65 and counts.index(suggestion[0]) <= 100) else query
