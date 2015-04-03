import webapp2
import jinja2
import os

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


application = webapp2.WSGIApplication([
	('/', mainpage)
	],debug=True)