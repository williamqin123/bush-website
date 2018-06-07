import webapp2, datetime
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

setup = '''<html>
			<head>
			<meta charset="UTF-8">
			<link href="style.css" rel="stylesheet">
			<link href="http://fonts.googleapis.com/css?family=Open+Sans:400,300" rel="stylesheet">
			<script src="script.js"></script>
			</head>
			<body id="body"><h1>Bush Elementary News Start Screen</h1>
			<nav>
			<a href="/news">News</a>
			<a href="/classes">Classes</a>
			<a href="/calendar">Events</a>
			<a href="/pto">PTO</a>
			<a href="/memories">Grade Memories</a>
			</nav>'''

form = '''<div class="teachers"><form method="post">
					<div class="formcontain">
						<input type="text" name="%s">%s</div>
					<div class="formcontain">
						<input type="text" name="%s">%s
					</div>
					<textarea placeholder="%s" name="%s"></textarea><br>
					<input type="submit">
				</form></div>'''

foot ='''
<img src="hisd.png" width="300" height="90"></body></html>
'''

cal = '''<table class="calendar">
<tr class="control">
<td>SUNDAY</td><td>MONDAY</td><td>TUESDAY</td><td>WEDNESDAY</td><td>THURSDAY</td><td>FRIDAY</td><td>SATURDAY</td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
<tr>
<td></td><td></td><td></td><td></td><td></td><td></td><td></td>
</tr>
</table>'''

def key(pagename):
	return ndb.Key("NewsArticle", pagename)

class Html(ndb.Model):
	name = ndb.StringProperty()
	content = ndb.TextProperty()
	image = ndb.StringProperty()
	day = ndb.IntegerProperty()
	month = ndb.IntegerProperty()
	year = ndb.IntegerProperty()

class DescriptionMemory(webapp2.RequestHandler):

	def post(self):
		grade = Html(parent = key(self.request.get("name")))
		grade.name = self.request.get("name")
		grade.image = self.request.get("image")
		grade.content = self.request.get("content")
		grade.put()
		self.redirect("/memories")
	
	def get(self):
		self.response.write(setup)
		fstgrade = Html.query(ancestor = key("1"))
		sndgrade = Html.query(ancestor = key("2"))
		trdgrade = Html.query(ancestor = key("3"))
		fthgrade = Html.query(ancestor = key("4"))
		ithgrade = Html.query(ancestor = key("5"))
		grades = [fstgrade, sndgrade, trdgrade, fthgrade, ithgrade]

		for eachgrade in grades:
			if (len(eachgrade.fetch(5)) > 0):
				self.response.write("<h2>Stuff About Grade %s</h2>" % eachgrade.fetch(999)[0].name)
				for entry in eachgrade.fetch(999):
					self.response.write("<h3>%s</h3>%s" % (entry.image, entry.content))

		self.response.write(form % ("name", "Grade", "image", "Year", "Cool stuff", "content"))
		self.response.write(foot)
		
class PTOpage(webapp2.RequestHandler):

	def post(self):
		person = Html(parent = key("person"))
		person.name = self.request.get("name")
		person.image = self.request.get("image")
		person.content = self.request.get("content")
		person.put()
		self.redirect("/pto")

	def get(self):
		self.response.write(setup)
		people = Html.query(ancestor = key("person"))
		self.response.write("<table class='pro'>")
		for person in people.fetch(999):
			self.response.write("<tr><td>%s</td><td>%s</td><td><section>%s</section></td></tr>" % (person.image, person.name, person.content))

		self.response.write("</table>")

		self.response.write(form % ("name", "Name", "image", "Part of PTO", "Description", "content"))
		self.response.write(foot)

class Calendar(webapp2.RequestHandler):

	def post(self):
		if len(self.request.get("newmonth", "__init__")) == 0:
			for y in Html.query(ancestor = key("event")).fetch(31):
				y.key.delete()
			month = Html(parent = key("month"))
			month.name = self.request.get("name")
			month.put()

		else:
			event = Html(parent = key("event"))
			event.name = self.request.get("name")
			event.content = self.request.get("content")
			event.day = int(self.request.get("day"))
			event.put()
		self.redirect("/calendar")

	def get(self):
		days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
		months = {"01" : 31, "02" : 30, "03" : 31, "04" : 30, "05" : 31, "06" : 31, "07" : 30, "08" : 31, "09" : 30, "10" : 31, "11" : 30, "12" : 31}
		self.response.write(setup)
		self.response.write(cal)
		self.response.write(form % ("day", "Day Number", "name", "Title", "Event", "content"))
		self.response.write(form % ("content", "Month", "name", "1st Day of Month", "Erase Data", "newmonth"))
		events = Html.query(ancestor = key("event"))
		offset = 1
		monthname = Html.query(ancestor = key("month")).fetch(1)
		if len(monthname) > 0:
			offset = days.index(monthname[0].name)

		self.response.write('''<script>
			var tds=document.getElementsByTagName("TD");
			tds[%s].style.backgroundColor="rgb(189, 49, 33)";
			for (x=%s; x<%s; x++) {
				tds[x+7].innerHTML="<h2>"+parseInt(x+1-%s).toString()+"</h2>";
			}
			for (x=0; x<%s; x++) {
				tds[x+7].style.backgroundColor="lightgray";
			}
			</script>''' % (str(int(unicode(datetime.datetime.now())[8:10]) + offset + 7), offset, str(months[unicode(datetime.datetime.now())[5:7]] + offset), offset, offset))
		for day in events.fetch(31):
			self.response.write('''<script>
				var tds=document.getElementsByTagName("TD");
				tds[%s].innerHTML="%s";
				</script>''' % (str(offset + 7 + day.day), day.content))

		self.response.write(foot)

class MainHandler(webapp2.RequestHandler):

	def post(self):
		page = Html.query(ancestor = key("news"))

		htmlpage = Html(parent = key("news"))
		htmlpage.name = self.request.get("name")
		htmlpage.content = self.request.get("content")
		htmlpage.day = int(self.request.get("date")[:2])
		htmlpage.month = int(self.request.get("date")[3:5])
		htmlpage.year = int(self.request.get("date")[6:])
		htmlpage.put()
		self.redirect("/news")

	def get(self):
		page = Html.query(ancestor = key("news")).order(-Html.day).order(-Html.month).order(-Html.year)

		self.response.write(setup)
		self.response.write("<section>")
		allnews = ""
		for x in page.fetch(999):
			contenthtml = "<article class='news' style='background-image: url(%s)'><time>%s</time><h1>%s</h1>%s</article>" % (x.image, "%s/%s/%s" % (x.day, x.month, x.year), x.name, x.content)
			if page.fetch(999).index(x) < 3:
				self.response.write(contenthtml)
			allnews = allnews + contenthtml.replace("'", "\\'")

		self.response.write('''
			<a href="#" onclick="news('%s')">See all news</a>
			<a href="#" onclick="window.location='http://www.houstonisd.org/bushelem'">Go to previous version</a>
			</section>
				%s
			%s
			''' % (allnews, form % ("date", "Date", "name", "Title", "Content", "content"), foot))

class Classrooms(webapp2.RequestHandler):

	def get(self):
		self.response.write(setup)
		htmltxt = open("static/classes.html", "r")
		for txt in htmltxt.readlines():
			self.response.write(txt.replace("\n", "").replace("\t", ""))

		htmltxt.close()

app = webapp2.WSGIApplication([
	("/classes", Classrooms),
	("/news", MainHandler),
	("/calendar", Calendar),
	("/pto", PTOpage),
	("/memories", DescriptionMemory)
], debug = True)
