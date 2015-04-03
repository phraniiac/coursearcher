from google.appengine.api import search
from google.appengine.ext import ndb
import datastore as ds
import urlfuncs as ul
import copy
from google.appengine.api import users


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

def makeany():
	docindex = search.Index(name = "mitocw")
	docindex1 = search.Index(name = "alldomains")
	document_ids = docindex.get_range(limit=300,deadline=None)
	while True:
		#return document_ids
		if len(document_ids) == None:
			break
		for x in document_ids:
			docindex1.put(x)
		document_ids = docindex.get_range(start_id=document_ids[3].doc_id,limit=300,deadline=None)
		#docindex.delete(document_ids)

def makedoc(url,domain):
	if domain != "edx":
		Link = ul.extractInfo(url,domain)
	else:
		Link = ul.extractInfoEdX(url,domain)
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
		index = search.Index(name = domain)
		index.put(documentlist)
		documentlist = []

def deleteindexes(domain):
	"""Delete all the docs in the given index."""
	docindex = search.Index(name = domain)
	try:
		while True:
		# until no more documents, get a list of documents,
		# constraining the returned objects to contain only the doc ids,
		# extract the doc ids, and delete the docs.
			document_ids = [document.doc_id
							for document in docindex.get_range(ids_only=True,limit=200)]
			if not document_ids:
				break
			docindex.delete(document_ids)
	except search.Error:
		logging.exception("Error removing documents:")

######## Result Functions ########


def fetchresult(query_string,domain):
	#updatequeryentry(query_string)
	docindex = search.Index(name = domain)
	ListOfLinkObjects = []
	try:
		query_options = search.QueryOptions(limit = 200)
		query = search.Query(query_string=query_string, options=query_options)
		search_results = docindex.search(query,deadline=None)
		number_found = search_results.number_found
		returned_count = len(search_results.results)
		i = 0
		listob = []
		for x in search_results:
			listob.append(x.fields)
			i += 1
			if i == 10:
				i = 0
				listOb = copy.deepcopy(listob)
				listob = []
				ListOfLinkObjects.append(listOb)
		if len(listob) > 0:
			listOb = copy.deepcopy(listob)
			ListOfLinkObjects.append(listOb)
		return ListOfLinkObjects,number_found,returned_count
	except Exception:
		return [],0,0

def updatequeryentry(query):
	qry = ds.querysearched.query(ds.querysearched.keyword == query.lower()).get()
	if qry == None:
		qs = ds.querysearched()
		qs.keyword = query.lower()
		qs.count = 1
		qs.put()
	else:
		qry.count += 1
		qry.put()

########### login #########

def checklogin():
	user = users.get_current_user()
	if user:
		if users.is_current_user_admin():
			return 1
		else:
			return 0
