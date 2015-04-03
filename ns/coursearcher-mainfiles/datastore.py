from google.appengine.ext import ndb
import json
import dsfunc
import time

mostkeys = {
		"and":1,
		"there":1,
		"this":1,
		"how":1,
		"now":1,
		"the":1
		}

class Keywords(ndb.Model):
	""" database table for keywords """
	keyword = ndb.StringProperty(indexed = True)
	ListOfLinks = ndb.StringProperty()		# List in JSON.

class Links(ndb.Model):
	"""database table for Links"""
	link = ndb.StringProperty()
	
def makejson(ListOfLinks):
	""" makes json format of the python list passed to it."""
	return json.dumps(ListOfLinks)

def givelist(string):
	""" returns the normal python list from json format."""
	return json.loads(string)

def returndict(keyword):
	""" return """
	qry = Keywords.query(Keywords.keyword == keyword).get()
	if qry != None:
		return givelist(qry.ListOfLinks)
	else:
		return None

def getDesc(x):
	""" Gets the description of the link."""
	qry = Links.query(Links.link == x).get()
	if qry:
		return qry.desc
	else:
		return None

def gettitle(x):
	""" Gets the title of the link."""
	qry = Links.query(Links.link == x).get()
	if qry:
		return qry.pagetitle
	else:
		return None

def updatekeyword(link):
	""" puts the distinct keywords in the table in the datastore"""
	pagetitle = link.pagetitle
	desc = link.desc
	keywords = dsfunc.refinehtml(pagetitle,desc)
	for x in keywords:
		##	Check if it already exists.
		##	And also that keyword is greater than or equal to length 3.
		if len(x) >= 3 and x.lower() not in mostkeys:
			qry = Keywords.query(Keywords.keyword == x.lower()).get()
			if qry == None:
				keyword = Keywords()
				keyword.keyword = dsfunc.refinekeyword(x)
				keyword.ListOfLinks = makejson([link.link])
				keyword.put()
			else:
				if link.link not in list(givelist(qry.ListOfLinks)) and x.lower() not in mostkeys:
					listOfLinks = givelist(qry.ListOfLinks) + [link.link]
					qry.ListOfLinks = makejson(listOfLinks)
					qry.put()

def updatedata(ListOfLinks):
	""" Updates the keywords and title in the table in datastore."""
	for x in ListOfLinks:
		x = dsfunc.extractInfo(x)
		updatekeyword(x)
		x.flag = 1
		x.put()

def addtolist(ListOfLinks):
	""" Adds the links inititally to the table in datastore"""
	for x in ListOfLinks:
		qry = Links.query(Links.link == x).get()
		if qry == None:
			link = Links()
			link.link = x
			link.flag = 0
			link.put()

def returnobject(linklist):
	return Links.query(Links.link == linklist[0]).get()

def getlinks(flagvalue,numlinks):
	qry = Links.query(Links.flag == flagvalue).fetch(numlinks)
	return qry

def resetdatastore():
	ndb.delete_multi(Links.query().fetch(keys_only=True))
	ndb.delete_multi(Keywords.query().fetch(keys_only=True))

