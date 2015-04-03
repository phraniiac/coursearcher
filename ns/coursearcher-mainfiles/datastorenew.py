from google.appengine.api import search
from google.appengine.ext import ndb
import dsfunc

class LinksForNDB(ndb.Model):
	"""database table for Links"""
	link = ndb.StringProperty()	
	flag = ndb.IntegerProperty()	

class querysearched(ndb.Model):
	querystring = ndb.StringProperty()
	count = ndb.IntegerProperty()

class Links():
	link = ""
	pagetitle = ""
	desc = ""

def updatequery(queryuser):
	qry = querysearched.query(querysearched.querystring == queryuser.lower()).get()
	qs = querysearched()
	if qry == None:
		qs = querysearched()
		qs.querystring = queryuser.lower()
		qs.count = 1
	else:
		qs = qry
		qs.count += 1
	qs.put()

def makedoc(link):
	Link = Links()
	Link = dsfunc.extractInfo(link)
	Link.link = link
	document = search.Document(
	fields = [
		search.TextField(name='link',value=str(Link.link)),
		search.TextField(name='title',value=str(Link.pagetitle)),
		search.TextField(name='description',value=str(Link.desc))
	])
	return document

def addtotable(ListOfLinks):
	for x in ListOfLinks:
		qry = LinksForNDB.query(LinksForNDB.link == x).get()
		if qry == None:
			link = LinksForNDB()
			link.link = str(x)
			link.flag = 0
			link.put()

def makeindex():
	qry = LinksForNDB.query(LinksForNDB.flag == 0).fetch(50)
	linklist = []
	if qry != None:
		for x in qry:
			linklist.append(x.link)
			x.flag = 1
			x.put()
		updatedata(linklist)
		return 1
	else:
		return 0

def updatedata(ListOfLinks):
	documentlist = []
	while len(ListOfLinks) > 0:
		for x in range(0,195):
			if x < len(ListOfLinks):
				documentlist.append(makedoc(str(ListOfLinks[x])))
				ListOfLinks.remove(ListOfLinks[x])
				if len(ListOfLinks) == 0:
					break
			else:
				break
		index = search.Index(name = "SearchLinks")
		index.put(documentlist)
		documentlist = []

def resultreturn(querystr):
	try:
		index = search.Index(name = "SearchLinks")
		search_results = index.search(querystr)
		number_found = search_results.number_found
		returned_count = len(search_results.results)
		ListOfLinkObjects = []
		for x in search_results:
			ListOfLinkObjects.append(x.fields)
		return ListOfLinkObjects,number_found,returned_count
	except search.Error:
		return search.Error

def resetdatastore():
	qry = LinksForNDB.query(LinksForNDB.flag == 1).fetch()
	while len(qry) > 0:
		qry[0].flag = 0
		qry[0].put()
		qry = LinksForNDB.query(LinksForNDB.flag == 1).fetch()