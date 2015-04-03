import urllib2
from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as ET

def refinexml(xml):
	links = []
	root = ET.fromstring(xml)
	for link in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
		links.append(link.text)
	return links

def getlinks(link):
	xml = validlink(link)
	l = [1]
	if xml:
		return refinexml(xml)
	else:
		return l

def validlink(link):
	try:
		response = urlopen(link)
		return str(response.read())
	except URLError, e:
		if hasattr(e, 'reason'):
			print 'We failed to reach server.'
			print 'Reason: ', e.reason
			return False
		elif hasattr(e, 'code'):
			print 'The server couldn\'t fulfill the request'
			print 'Error code: ', e.code
			return False
		else:
			return str(response.read())

def main():
	start_link = raw_input("Enter Url : ")
	linkslist = getlinks(start_link)
	if linkslist:
		print "Successful"
		print len(linkslist)
	else:
		print "Defected URL"

if __name__ == "__main__":
	main()