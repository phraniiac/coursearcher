import webapp2
import jinja2
import os
from src import funcs as fs
from google.appengine.api import users

user = users.get_current_user()

template_dir = os.path.join(os.path.dirname(__file__),"html")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

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

class mainpage(Handler):
	def get(self):
		self.render('mainpage.html')

class result(Handler):
	"""docstring for result"""
	def get(self):
		query = self.getvar("q")
		domain = str(self.getvar("opt"))
		number_found = 0
		returned_count = 0
		resLinks = [[]]
		cursor = int(self.getvar("cursor"))
		if len(domain) <= 0 or len(query) <= 0 or domain == None:
			self.render('result.html',number_found=number_found,returned_count=returned_count,opt=domain,mainkeyword=query,cursor=cursor,total_pages=0)
		else:
			resLinks,number_found,returned_count = fs.fetchresult(query,domain)
			total_pages = int(returned_count/10)
			if total_pages%10 != 0:
				total_pages += 1
			if returned_count != 0:
				self.render('result.html',resLinks=resLinks[cursor],number_found=number_found,returned_count=returned_count,opt=domain,mainkeyword=query,cursor=cursor,total_pages=total_pages)
			else:
				self.render('result.html',resLinks=[],number_found=number_found,returned_count=returned_count,opt=domain,mainkeyword=query,cursor=cursor,total_pages=total_pages)

class addlinks(Handler):
	"""docstring for addlinks"""
	def get(self):
		if users.is_current_user_admin():
			self.render('addlinks.html',action="resaddlinks")
		else:
			self.response.write("Sorry!!!!")

class resaddlinks(Handler):
	"""docstring for addlinks"""
	def get(self):
		if fs.checklogin() == 1:
			domain = str(self.getvar("opt"))
			url = self.getvar("link")
			fs.putxmllinks(url,domain)
			self.response.write("Did!!!!")

class deleteall(Handler):
	"""docstring for deleteall"""
	def get(self):
		if fs.checklogin() == 1:
			self.render('deleteall.html')

class resdeleteall(Handler):
	"""docstring for resdeleteall"""
	def get(self):
		if fs.checklogin() == 1:
			domain = str(self.getvar("opt"))
			fs.deleteall(domain)
			self.response.write("Done!!!!!!!!!")

class makeindex(Handler):
	"""docstring for makeindex"""
	def get(self):
		if fs.checklogin() == 1:
			self.render('makeindex.html')

class resindex(Handler):
	"""docstring for resindex"""
	def get(self):
		domain = str(self.getvar("opt"))
		fs.makeindex(int(self.getvar("q")),domain)
		self.response.write("Done!!!!!!!")

class cronedx(Handler):
	"""docstring for cronedx"""
	def get(self):
		domain = "edx"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class cronmitocw(Handler):
	"""docstring for cronmitocw"""
	def get(self):
		domain = "mitocw"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class cronkhanacademy(Handler):
	"""docstring for cronkhanacademy"""
	def get(self):
		domain = "khanacademy"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class cronudemy(Handler):
	"""docstring for cronudemy"""
	def get(self):
		domain = "udemy"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class deleteindexes(Handler):
	"""docstring for deleteindexes"""
	def get(self):
		if fs.checklogin() == 1:
			domain = self.render('deleteindexes.html')

class deleteindexesres(Handler):
	"""docstring for deleteindexes"""
	def get(self):
		domain = str(self.getvar("opt"))
		fs.deleteindexes(domain)
		self.response.write("Done!!!!!!!!!!!!!!!")

class makeany(Handler):
	"""docstring for makeany"""
	def get(self):
		if fs.checklogin() == 1:
			fs.makeany()
			self.response.write("Done!!!")

class aboutproject(Handler):
	"""docstring for aboutproject"""
	def get(self):
		self.render("aboutproject.html")

application = webapp2.WSGIApplication([
	('/', mainpage),
	('/addlinks',addlinks),
	('/resaddlinks',resaddlinks),
	('/result',result),
	('/deleteall',deleteall),
	('/resdeleteall',resdeleteall),
	('/makeindex', makeindex),
	('/resindex',resindex),
	('/cronedx',cronedx),
	('/cronmitocw',cronmitocw),
	('/cronkhanacademy',cronkhanacademy),
	('/cronudemy',cronudemy),
	('/deleteindexes',deleteindexes),
	('/deleteindexesres',deleteindexesres),
	('/makeany',makeany),
	('/aboutproject',aboutproject)
	],debug=True)