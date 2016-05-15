import bottle
import cgi
import re

@bottle.route('/')
def index():
    return bottle.template('<b>Hello my friend</b>!')


bottle.debug(True)
bottle.run(host='localhost', port=8082)
