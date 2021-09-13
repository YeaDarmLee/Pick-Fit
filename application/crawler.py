from flask import Flask, render_template
from flask import Blueprint

# import dbModule
from application import dbModule

crawler = Blueprint("crawler", __name__, url_prefix="/crawler")

#crawler 
@crawler.route("/")
def index():
  return render_template('crawler/index.html')

# API
# searchTemplate
@crawler.route('/search')
def searchTample():

  db_class = dbModule.Database()
  search_url_info = "SELECT * FROM url_info;"
  url_info_result = db_class.executeAll(search_url_info)

  result = []
  for i in url_info_result:
    result.append(i)

  return {'result': result}