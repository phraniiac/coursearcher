from google.appengine.ext import ndb
import funcs

class Links(ndb.Model):
	"""docstring for Links"""
	Link = ndb.StringProperty()
	Flag = ndb.IntegerProperty()
			

class khanacademylinks(Links):
	"""docstring for khanacademylinks"""

class mitocwlinks(Links):
	"""docstring for mitocwlinks"""

class edxlinks(Links):
	"""docstring for edxlinks"""

class udemylinks(Links):
	"""docstring for udemy"""

class udacitylinks(Links):
	"""docstring for udacity"""						

class querysearched(ndb.Model):
	"""docstring for querysearched"""
	keyword = ndb.StringProperty()
	count = ndb.IntegerProperty()
	lastsearch = ndb.DateTimeProperty(auto_now = True)
