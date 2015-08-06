#!/usr/bin/env python
import web, sys, MySQLdb

host= 'localhost'
user = 'monitor'
password = 'monitor'

urls = (
  '/', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

class Index(object):
    def GET(self):
        return render.comic_form()

    def POST(self):
        form = web.input(name="Nobody", greet="Hello")
        greeting = "%s, %s" % (form.character, form.title)
        return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()
