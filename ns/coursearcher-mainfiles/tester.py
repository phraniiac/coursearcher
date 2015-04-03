from urllib2 import urlopen
import xml.etree.ElementTree as ET

def refinehtmltags(html):  # html as string
    startpos = 0
    endpos = 0
    while html.find('<script') != -1:
        startpos = html.find('<script')
        endpos = html.find('</script>')
        #print startpos, endpos
        html = html[:startpos] + html[endpos + 9:]
    while html.find('<style') != -1:
        startpos = html.find('<style')
        endpos = html.find('</style>')
        #print startpos, endpos
        html = html[:startpos] + html[endpos + 7:]
    while html.find('<!--') != -1:
        startpos = html.find('<!--')
        endpos = html.find('-->')
        #print startpos, endpos
        html = html[:startpos] + html[endpos + 3:]
    while html.find('<a') != -1:
        startpos = html.find('<a')
        endpos = html.find('</a>')
        #print startpos, endpos
        html = html[:startpos] + html[endpos + 4:]
    while html.find('<div') != -1:
        startpos = html.find('<div')
        endpos = html[startpos:].find('</div>')
        #print startpos, endpos
        html = html[:startpos] + html[endpos + 6:]
    return html
    #print html
    #remove styles

def refinehtml(pagetitle, desc):
	keywords = []
	titlekeywords = pagetitle.split(" ")
	desckeywords = desc.split(" ")
	keywords = unionlists(titlekeywords,desckeywords)
	return keywords

def xmlextractor(url):
	"""Gets the url and returns the List of links present in the whole xml"""
	ListOfLinks = []
	response = urlopen(url)
	root = ET.fromstring(response.read())
	for link in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
		ListOfLinks.append(link.text)
	return ListOfLinks

def extractInfo(Link):
    """Gets the link of the page, and returns Page title and Description of the Link"""
    response = urlopen(Link)
    html = response.read()
    #LinkInfo = ds.Links()
    #html = refinehtmltags(html)
    pagetitle = html[html.find('<title>') + 7 : html.find('</title>')]
    startindex = html.find('<meta name="description" content="')
    desc = html[startindex + 34 : html.find('"',startindex + 38)]
    print pagetitle
    print desc
    #### Use the links to
    #### Extract the information as
    #### pagetitle
    #### description
    #return LinkInfo

#print xmlextractor("https://www.khanacademy.org/sitemap.xml")
extractInfo("http://www.udacity.com")