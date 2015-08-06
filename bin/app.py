#!/usr/bin/env python
import web, sys, MySQLdb, subprocess

host = 'localhost'
user = 'monitor'
password = 'monitor'

urls = (
  '/', 'Index',
  '/Tye', 'Tye'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")
render2 = web.template.render('templates/', base="layout2")

class Index(object):
    def GET(self):
        return render.comic_form()

    def POST(self):
	conn = MySQLdb.Connection(db='comics', host=host, user=user, passwd=password)
	mysql = conn.cursor()
        form = web.input(title="null", character="null")
        if form.title != "":
		mysql.execute("""SELECT title, volume, issue, approx_price, description FROM comickeys WHERE title LIKE '%%%s%%' """ % form.title)
	elif form.character !="":
		mysql.execute("""SELECT title, volume, issue, approx_price, description FROM comickeys WHERE description LIKE '%%%s%%' """ % form.character)
	#mysql.execute(sql)
	fields=mysql.fetchall()
	content='<table border="1" align=left><tr><th>Title</th><th>Volume</th><th>Issue</th><th>Approx Value</th><th>Description</th></tr><tbody>'
	for field in fields:
		title = str(field[0])
        	volume = str(field[1])
        	issue = str(field[2])
        	approx_price = str(field[3])
        	description = str(field[4])
        	content = content + '<tr><td>' + title + '</td><td>' + volume + '</td><td>' + issue + '</td><td>' + approx_price + '</td><td>' + description + '</td></tr>'
	content = content + '</tbody></table>'
	with open("comic_log", "a") as myfile:
	    	myfile.write( web.ctx['ip'] + " | Form Char - " + form.character + "| Form Title - " + form.title + "\n")       
	mysql.close()
	conn.close()
	return render.index(content = content)

class Tye(object):
    def GET(self):
        return render2.fm_form()

    def POST(self):
        form = web.input(erikmoney="null", ryanmoney="null")
        if form.erikmoney != "":
	#	subprocess.call("/bin/bash /home/1y3/bin/erikmoney.sh " + form.erikmoney)
		subprocess.Popen(['/home/1y3/bin/erikmoney.sh %s' % form.erikmoney], shell = True)
	elif form.ryanmoney !="":
		subprocess.Popen(['/home/1y3/bin/ryanmoney.sh %s' % form.ryanmoney], shell = True)
	return render2.fm_form()

if __name__ == "__main__":
    app.run()
