from urllib2 import urlopen
import xml.etree.ElementTree as ET
import funcs as fs
from bs4 import BeautifulSoup as bsp

def xmlextractor(url):
	"""Gets the url and returns the List of links present in the whole xml.
	Normally valid for linktype - khan academy, EdX, Udemy and OCW.
	"""
	ListOfLinks = []
	response = urlopen(url)
	root = ET.fromstring(response.read())
	for link in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
		ListOfLinks.append(link.text)
	return ListOfLinks

def extractInfo(Link,domain):
	"""Gets the link of the page, and returns Page title and Description of the Link
	works for - 
	khan academy
	EdX
	udacity
	Udemy
	"""
	LinkInfo = fs.Links()
	LinkInfo.link = Link
	try:
		response = urlopen(Link)
		html = response.read()
		sp = bsp(html)
		if domain != 'mitocw':
			desc = sp.findAll(attrs={"name":"description"})
		else:
			desc = sp.findAll(attrs={"name":"Description"})
		LinkInfo.pagetitle = sp.title.text.decode("utf-8")
		LinkInfo.desc = desc[0]['content'].decode("utf-8")
	except Exception:
		LinkInfo.pagetitle = "pagetitle"
		LinkInfo.desc = "desc[:498]"
	return LinkInfo