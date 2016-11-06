import json
import os
import logging
import copy
import requests
import pprint
import string, random
import datetime
from urlparse import urlparse
from flask import Flask, request, render_template, make_response
from jinja2 import Environment, PackageLoader
import local_settings
logging.basicConfig()

# Loading initial config
config = local_settings.env
app = Flask(__name__)
template_env = Environment(loader=PackageLoader('api_routes', 'templates'))

# Used to display errors on webpage       
@app.errorhandler( 500 )
def internal_500_error( exception ):
     app.logger.exception( exception )
     return pprint.pformat( exception ), 500

@app.errorhandler( 404 )
def internal_404_error( exception ):
     app.logger.exception( exception )
     return 'Portal<br/>\n%s<br/>\n%s' % ( exception, request.url ), 404

@app.errorhandler( 401 )
def internal_401_error( exception ):
     app.logger.exception( exception )
     return 'Portal<br/>\n%s<br/>\n%s' % ( exception, request.url ), 401

@app.route('/', methods=['GET'])
def index( ):
    url = request.url_root
    domain_name = urlparse(url).netloc

    username = request.headers.get('X-Username', None)
    if username == 'billy':
         admin = True
    else:
         admin = False

    # get content
    # content = theme.get_content(domain, document)
    content = None
    
    if not content:
         content = {}
         
    payload = {
         "domain": domain_name
    }
    return render_template('index.html', payload=payload, content=content, admin=admin)

@app.route('/<page>.html', methods=['GET'])
def page( page ):
    url = request.url_root
    domain_name = urlparse(url).netloc

    username = request.headers.get('X-Username', None)
    if username in 'billy':
         admin = True
    else:
         admin = False

    # get content
    # content = theme.get_content(domain, document)
    content = None
    
    if not content:
         content = {}

    payload = {
         "domain": domain_name
    }
    return render_template('%s.html' % page, payload=payload, content=content, admin=admin)

@app.route("/save_page", methods=['POST'])
def save_page():
     content  = request.form
     domain_name = urlparse(dict(request.headers).get('Referer')).netloc
     # domain = theme.admin_check(domain_name)
     path = urlparse(dict(request.headers).get('Referer')).path
     document =  {
          "content":content,
          "meta": {
               "domain": domain_name,
               "path": path
          }
     }
     # status = theme.save_content(domain, document)
     return 'saved'

if __name__ == "__main__":
     pass
else:
     app.root_path = config.get( 'HOME_DIR' )
