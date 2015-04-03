from urllib2 import urlopen
import xml.etree.ElementTree as ET
import datastore as ds
import time

def refinehtmltags(html):  # html as string
    """ Takes html as string and returns the string without
        the html tags like <script>, <style>, and html comments"""
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
    f = open('html','w')
    f.write(html)

def refinehtml(pagetitle, desc):
    """ returns all the keywords present in the title and 
        the meta description of the page """
    keywords = []
    titlekeywords = pagetitle.split(" ")
    desckeywords = desc.split(" ")
    keywords = unionlists(titlekeywords, desckeywords)
    return keywords

def refinekeyword(keyword):
    """ refines the keywords from '.' and ',' """
    while keyword.find(',') != -1:
        keyword = keyword[:keyword.find(',')]+keyword[keyword.find(',')+1:]
    while keyword.find('.') != -1:
        keyword = keyword[:keyword.find('.')]+keyword[keyword.find('.')+1:]
    return keyword.lower()

def unionlists(a, ListOfLinks):
    """ Takes 2 lists, link1 and link2, and returns the unionlist of of both of them."""
    for x in a:
        if x not in ListOfLinks or len(ListOfLinks) == 0:
            ListOfLinks.append(x)
    return ListOfLinks


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
    LinkInfo = ds.Links()
    LinkInfo.link = Link
    try:
        response = urlopen(Link)
        html = response.read()
        pagetitle = html[html.find('<title>') + 7 : html.find('</title>')]
        startindex = html.find('<meta name="description" content="')
        desc = html[startindex + 34 : html.find('"',startindex + 38)]
        LinkInfo.pagetitle = pagetitle
        LinkInfo.desc = desc[:498]
    except Exception:
        LinkInfo.pagetitle = "pagetitle"
        LinkInfo.desc = "desc[:498]"
    return LinkInfo