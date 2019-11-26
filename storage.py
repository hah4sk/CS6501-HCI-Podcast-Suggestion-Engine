import mysql.connector as connector
from mysql.connector import errorcode
import pickle

#Apparently write_frame is deprecated because fuck me
from sqlalchemy import create_engine


class PodcatDB:
	tables = {}
	tables['weekly_podcast_threads'] = (
	    "CREATE TABLE `weekly_podcast_threads` ("
	    "  `id` varchar(11) NOT NULL,"
	    "  `ts` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
	    "  PRIMARY KEY (`id`)"
	    ") ENGINE=InnoDB")

	#######################
	#                     #                  
	#   Setup functions   #                  
	#                     #                  
	#######################

	def __init__(self):
		self._setup()
	def __del__(self):
		self._close()

	def _setup(self):
		self.db_name = 'podcats'
		self.cnx = self._connect()
		self.c = self.cnx.cursor()
		self._create_db()
		self._create_tables()
		self._commit()

	def _close(self):
		self._commit()
		#self.c.close()
		#self.cnx.close()

	#TODO: Abstract config into an ini file
	def _connect(self):
		config = {
			"host":"localhost",
			"user":"podcat",
			"password":"podcat"
		}
		try:
			c = connector.connect(**config)
			return c
		except:
			print("[storage] Error connecting to sqlserver")
			exit(1)

	def _create_db(self):
		try:
		    self.c.execute("USE {}".format(self.db_name))
		except connector.Error as err:
			print("[storage] Database {} does not exist".format(self.db_name))
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				try:
					self.c.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name))
				except connector.Error as err:
					print("[storage] Failed creating database: {}".format(err))
					exit(1)
				print("[storage] Database {} created successfully.".format(self.db_name))
				self.cnx.database = self.db_name
			else:
				print(err)
				exit(1)

	def _create_tables(self):
		for t in self.tables:
		    tspec = self.tables[t]
		    try:
		        print("[storage] Creating table {}: ".format(t), end='')
		        self.c.execute(tspec)
		    except connector.Error as err:
		        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
		            print("already exists.")
		        else:
		            print(err.msg)
		    else:
		        print("OK")

	#######################
	#                     #                  
	#  Utility functions  #                  
	#                     #                  
	#######################

	def _commit(self):
		self.cnx.commit()

	def _rollback(self):
		self.cnx.rollback()

	def drop(self, table): 
		try:
			self.c.execute("DROP TABLE {}.{}".format(self.db_name, table))
			self._commit()
		except connector.Error as err:
			print("[storage] Failed to drop table {}: {}".format(table, err))

	def get_all(self, table):
		try:
			self.c.execute("SELECT * FROM {}.{}".format(self.db_name, table))
			return self.c.fetchall()
		except connector.Error as err:
			print("[storage] Failed to select all from {}: {}".format(table, err))

	def exec(self, cmd): 
		try:
			self.c.execute(cmd)
			self._commit()
		except connector.Error as err:
			print("[storage] Failed exec: {}".format(table, err))


	#######################
	#                     #                  
	#   Data functions    #                  
	#                     #                  
	#######################

	def write_weekly_posts(self, arr):
		print("[storage] Updating weekly_podcast_threads:", end='')
		if(len(arr) == len(self.get_all("weekly_podcast_threads"))):
			print("already up to date")
		else:
			for item in arr:
				try:
					self.c.execute('INSERT into weekly_podcast_threads(id) VALUES(%s)', (item.id,))
				except connector.Error as err:
					print("failed: {}".format(err))
					self._rollback()
					exit(1)
				else:
					print('OK')
			self._commit()

	#Using a local pickle as it's less clunky and I don't really want temp tables, final gets written
	def load_df(self, name):
		try:
		    df = pickle.load(open("{}.pickle".format(name), "rb"))
		    print("[storage] Previous run found; loading '{}'".format(name))
		    return df
		except (OSError, IOError) as e:
			print("[storage] No previous df '{}'".format(name))
		    
	def save_df(self, df, name):
		print("[storage] Saving '{}'".format(name))
		pickle.dump(df, open("{}.pickle".format(name), "wb"))

	def write_fuzzy_df(self, df):
		print("[storage] Updating fuzzy_podcast_info:", end='')
		try:
			engine = create_engine('mysql+mysqlconnector://podcat:podcat@localhost/podcats', echo=False)
			df.to_sql(name='fuzzy_podcast_info', con=engine, if_exists = 'replace')
		except Exception as err:
			print("failed: {}".format(err))
		else:
			print("OK")












