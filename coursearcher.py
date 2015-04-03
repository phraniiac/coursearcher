import webapp2
import jinja2
import os
from src import funcs as fs


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
		res = fs.fetchresult(query,domain)
		self.render('result.html')

class addlinks(Handler):
	"""docstring for addlinks"""
	def get(self):
		self.render('addlinks.html',action="resaddlinks")

class resaddlinks(Handler):
	"""docstring for addlinks"""
	def get(self):
		domain = str(self.getvar("opt"))
		url = self.getvar("link")
		fs.putxmllinks(url,domain)
		self.response.write("Did!!!!")

class deleteall(Handler):
	"""docstring for deleteall"""
	def get(self):
		self.render('deleteall.html')

class resdeleteall(Handler):
	"""docstring for resdeleteall"""
	def get(self):
		domain = str(self.getvar("opt"))
		fs.deleteall(domain)
		self.response.write("Done!!!!!!!!!")

class makeindex(Handler):
	"""docstring for makeindex"""
	def get(self):
		self.render('makeindex.html')

class resindex(Handler):
	"""docstring for resindex"""
	def get(self):
		domain = str(self.getvar("opt"))
		fs.makeindex(int(self.getvar("q")),domain)
		self.response.write("Done!!!!!!!")

class cronindexingedx(Handler):
	"""docstring for cronindexingedx"""
	def get(self):
		domain = "edx"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class cronindexingmitocw(Handler):
	"""docstring for cronindexingmitocw"""
	def get(self):
		domain = "mitocw"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class cronindexingkhanacademy(Handler):
	"""docstring for cronindexingkhanacademy"""
	def get(self):
		domain = "khanacademy"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

class cronindexingudemy(Handler):
	"""docstring for cronindexingudemy"""
	def get(self):
		domain = "udemy"
		fs.makeindex(15,domain)
		self.response.write("Done!!!!!!!")

application = webapp2.WSGIApplication([
	('/', mainpage),
	('/addlinks',addlinks),
	('/resaddlinks',resaddlinks),
	('/result',result),
	('/deleteall',deleteall),
	('/resdeleteall',resdeleteall),
	('/makeindex', makeindex),
	('/resindex',resindex),
	('/cronindexingedx',cronindexingedx),
	('/cronindexingmitocw',cronindexingedx),
	('/cronindexingkhan',cronindexingkhanacademy),
	('/cronindexingudemy',cronindexingudemy)
	],debug=True)
