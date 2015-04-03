import urllib2
import os
from urllib2 import Request, urlopen, URLError

def refinehtml(html):	#html as string
	#remove scripts
	startpos = 0
	endpos = 0
	while html.find('<script>') != -1:
		startpos = html.find('<script>')
		endpos = html.find('</script>')
		html = html[:startpos] + html[endpos + 9:]
	f = open('html','w')
	f.write(html)
	print html
	#remove styles

def buildkeywords(link):
	html = urlopen(link).read()
	f = open('htmlold','w')
	f.write(str(html))
	refinehtml(str(html))

def main():
	link = "https://www.coursera.org/course/digitalmedia"
	buildkeywords(link)
	#html = """
	#<html>
	#<script>sdgvjkdgnjds</script>
	#vmkfgbm
	#<script>ovsgm</script>
	#</html>
	#"""
	#refinehtml(html)

if __name__ == "__main__" :
	main()