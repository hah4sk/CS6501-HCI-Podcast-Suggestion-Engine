from scrape import PPAW
from storage import PodcatDB
from fuzzy_manip import fuzzy_categories, fuzzy_titles, fuzz_ratio

if __name__ == '__main__':
	import pandas as pd
	db = PodcatDB()
	pc = PPAW()

	raw_df = db.load_df('raw_info')
	if not isinstance(raw_df, pd.DataFrame):
		posts = pc.get_posts()
		db.write_weekly_posts(posts)

		raw_df = pc.proc_posts(posts)
		db.save_df(raw_df, 'raw_info')

	#Apply fuzzy in a piecewise fashion due to lenghth
	f_df = db.load_df('fi_df')
	if not isinstance(f_df, pd.DataFrame):
		f_df = fuzzy_categories(raw_df, 15)
		db.save_df(f_df, 'fi_df')

	fuzzy_df = db.load_df('fuzzy_df')
	if not isinstance(fuzzy_df, pd.DataFrame):
		fuzzy_df = fuzzy_titles(f_df, 15)
		db.save_df(fuzzy_df, 'fuzzy_df')

	fuzz_ratio(fuzzy_df)
	db.write_fuzzy_df(fuzzy_df)
	print(fuzzy_df)





