import webapp2
import urllib2
import jinja2
import os
import datastore as ds
import datastorenew as dsnew
import dsfunc as dsfunc

template_dir = os.path.join(os.path.dirname(__file__),"html")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class ResultLinks():
	"""docstring for ResultLinks"""
	link = ''
	desc = ''
	pagetitle = 0

class Handler(webapp2.RequestHandler):
	def write(self, *a , **kw):
		self.response.out.write(*a, **kw)

	def getall(self , a):
		return self.request.get_all(a)

	def getvar(self, a):
		return self.request.get(a)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render("mainpage.html")

class Result(Handler):
	def get(self):
		queryterm = self.request.get("q")
		dsnew.updatequery(queryterm)
		ListOfLinkObjects = []
		number_found = 0
		returned_count = 0
		if len(queryterm) > 2:
			ListOfLinkObjects,number_found,returned_count = dsnew.resultreturn(queryterm)
		self.render("result.html",resLinks = ListOfLinkObjects,numcount = number_found, mainkeyword=queryterm, returnres=returned_count)


class UpdateByUrl(Handler):
	def get(self):
		action = "/dataurlupdater"
		self.render("dataupdater.html", action=action)

class UpdateByXml(Handler):
	"""docstring for UpdateData"""
	def get(self):
		action = "/dataxmlresult"
		self.render("dataupdater.html", action=action)

class UpdateXmlResult(Handler):
	"""docstring for UpdateResult"""
	def get(self):
		xmllink = self.request.get("xmllink")
		ListOfLinks = dsfunc.xmlextractor(xmllink)
		dsnew.addtotable(ListOfLinks)
		self.response.write("Did!!!!!!!!!!!")

class UpdateUrlResult(Handler):
	def get(self):
		link = self.request.get("xmllink")
		dsnew.updatedata([link])
		self.response.write("Did!!!!!!!!!!")

class resetall(Handler):
	"""docstring for resetall"""
	def get(self):
		dsnew.resetdatastore()
		self.response.write("Done Cleaning!")

class addlinks(Handler):
	def get(self):
		xmllink = self.request.get("xmllink")
		ListOfLinks = dsfunc.xmlextractor(xmllink)
		ds.addtolist(ListOfLinks)
		self.response.write("Did!!!!")

class cronindexing(Handler):
	def get(self):
		res = dsnew.makeindex()
		if res == 1:
			self.response.write("Success!!!")
		else:
			self.response.write("Failed!!!")

class aboutproject(Handler):
	def get(self):
		self.render("aboutproject.html")

class aboutme(Handler):
	def get(self):
		self.render("aboutme.html")

application = webapp2.WSGIApplication([
		('/',MainPage),
		('/result',Result),
		('/updatebyxml', UpdateByXml),
		('/dataxmlresult', UpdateXmlResult),
		('/updatebyurl', UpdateByUrl),
		('/dataurlupdater', UpdateUrlResult),
		('/resetall', resetall),
		('/addlinks',addlinks),
		('/cronindexing',cronindexing),
		('/aboutproject',aboutproject),
		('/aboutme',aboutme)
	],debug=True)