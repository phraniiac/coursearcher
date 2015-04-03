from google.appengine.api import search
from google.appengine.ext import ndb
import datastore as ds
import urlfuncs as ul


######## Writing Functions ########

def putxmllinks(url,domain):
	links = ul.xmlextractor(url)
	#links = []
	if domain == 'khanacademy':
		for link in links:
			qry = ds.khanacademylinks.query(ds.khanacademylinks.Link == link).get()
			if qry == None:
				kl = ds.khanacademylinks()
				kl.Link = link
				kl.Flag = 0
				kl.put()
	if domain == 'mitocw':
		for link in links:
			qry = ds.mitocwlinks.query(ds.mitocwlinks.Link == link).get()
			if qry == None:
				kl = ds.mitocwlinks()
				kl.Link = link
				kl.Flag = 0
				kl.put()
	if domain == 'edx':
		for link in links:
			qry = ds.edxlinks.query(ds.edxlinks.Link == link).get()
			if qry == None:
				kl = ds.edxlinks()
				kl.Link = link
				kl.Flag = 0
				kl.put()
	if domain == 'udemy':
		for link in links:
			qry = ds.udemylinks.query(ds.udemylinks.Link == link).get()
			if qry == None:
				kl = ds.udemylinks()
				kl.Link = link
				kl.Flag = 0
				kl.put()

def resetall(domain):
	if domain == 'khanacademy':
		qry = ds.khanacademylinks.query(khanacademylinks.Flag == 1).get()
		while qry != None:
			qry.Flag = 0
			qry.put()
			qry = ds.khanacademylinks.query(khanacademylinks.Flag == 1).get()
	if domain == 'edx':
		qry = ds.edxlinks.query(edxlinks.Flag == 1).get()
		while qry != None:
			qry.Flag = 0
			qry.put()
			qry = ds.edxlinks.query(edxlinks.Flag == 1).get()
	if domain == 'udemy':
		qry = ds.udemylinks.query(udemylinks.Flag == 1).get()
		while qry != None:
			qry.Flag = 0
			qry.put()
			qry = ds.udemylinks.query(udemylinks.Flag == 1).get()
	if domain == 'mitocw':
		qry = ds.mitocwlinks.query(mitocwlinks.Flag == 1).get()
		while qry != None:
			qry.Flag = 0
			qry.put()
			qry = ds.mitocwlinks.query(mitocwlinks.Flag == 1).get()


def deleteall(domain):
	if domain == 'khanacademy':
		ndb.delete_multi(ds.khanacademylinks.query().fetch(keys_only=True))
	if domain == 'edx':
		ndb.delete_multi(ds.edxlinks.query().fetch(keys_only=True))
	if domain == 'udemy':
		ndb.delete_multi(ds.udemylinks.query().fetch(keys_only=True))
	if domain == 'mitocw':
		ndb.delete_multi(ds.mitocwlinks.query().fetch(keys_only=True))


######## Query/Search API Functions #######

class Links():
	"""docstring for Links"""
	link = ""
	pagetitle = ""
	desc = ""	

def makedoc(url,domain):
	Link = ul.extractInfo(url,domain)
	Link.link = url
	document = search.Document(
	fields = [
		search.TextField(name='link',value=str(Link.link)),
		search.TextField(name='title',value=str(Link.pagetitle)),
		search.TextField(name='description',value=str(Link.desc))
	])
	return document

def makeindex(num,domain):
	if domain == 'khanacademy':
		qry = ds.khanacademylinks.query(ds.khanacademylinks.Flag == 0).fetch(num)
		linklist = []
		if qry != None:
			for x in qry:
				linklist.append(x.Link)
				x.Flag = 1
				x.put()
			updatedata(linklist,domain)
			return 1
		else:
			return 0
	if domain == 'edx':
		qry = ds.edxlinks.query(ds.edxlinks.Flag == 0).fetch(num)
		linklist = []
		if qry != None:
			for x in qry:
				linklist.append(x.Link)
				x.Flag = 1
				x.put()
			updatedata(linklist,domain)
			return 1
		else:
			return 0
	if domain == 'udemy':
		qry = ds.udemylinks.query(ds.udemylinks.Flag == 0).fetch(num)
		linklist = []
		if qry != None:
			for x in qry:
				linklist.append(x.Link)
				x.Flag = 1
				x.put()
			updatedata(linklist,domain)
			return 1
		else:
			return 0
	if domain == 'udacity':
		qry = ds.udacitylinks.query(ds.udacitylinks.Flag == 0).fetch(num)
		linklist = []
		if qry != None:
			for x in qry:
				linklist.append(x.Link)
				x.Flag = 1
				x.put()
			updatedata(linklist,domain)
			return 1
		else:
			return 0
	if domain == 'mitocw':
		qry = ds.mitocwlinks.query(ds.mitocwlinks.Flag == 0).fetch(num)
		linklist = []
		if qry != None:
			for x in qry:
				linklist.append(x.Link)
				x.Flag = 1
				x.put()
			updatedata(linklist,domain)
			return 1
		else:
			return 0

def updatedata(ListOfLinks,domain):
	documentlist = []
	while len(ListOfLinks) > 0:
		for x in range(0,195):
			if x < len(ListOfLinks):
				documentlist.append(makedoc(str(ListOfLinks[x]),domain))
				ListOfLinks.remove(ListOfLinks[x])
				if len(ListOfLinks) == 0:
					break
			else:
				break
		if domain == 'khanacademy':
			indexname = 'khanacademyindex'
		if domain == 'edx':
			indexname = 'edxindex'
		if domain == 'udemy':
			indexname = 'udemyindex'
		if domain == 'udacity':
			indexname = 'udacityindex'
		if domain == 'mitocw':
			indexname = 'mitocwindex'
		index = search.Index(name = domain)
		index.put(documentlist)
		documentlist = []

######## Result Functions ########


def fetchresult(query,domain):
	updatequeryentry(query)

	return []

def updatequeryentry(query):
	qry = ds.querysearched.query(ds.querysearched.keyword == query).get()
	if qry == None:
		qs = ds.querysearched()
		qs.keyword = query.lower()
		qs.count = 1
		qs.put()
	else:
		qry.count += 1
		qry.put()