from flask import Flask, render_template, request, escape, session
from flask import Blueprint

# import dbModule
from application import dbModule

recommend = Blueprint("recommend", __name__, url_prefix="/recommend")

# recommend
@recommend.route("")
def index():
  userid = '%s' % escape(session['user_id'])

  db_class = dbModule.Database()
  search_user = "SELECT * FROM user_info where id = '" + userid + "';"
  data = dict(db_class.executeOne(search_user))

  return render_template('recommend/recommend.html', result=data)

@recommend.route("/trend")
def trend():
  return render_template('recommend/trend.html')

@recommend.route("/clothe")
def clothe():
  return render_template('recommend/clothe.html')
  
@recommend.route("/keyword")
def keyword():
  return render_template('recommend/keyword.html')
  
@recommend.route("/statistic")
def statistic():
  return render_template('recommend/statistic.html')

