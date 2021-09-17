from flask import Flask, render_template, request, escape, session
from flask import Blueprint

# import dbModule
from application import dbModule

recommend = Blueprint("recommend", __name__, url_prefix="/recommend")

# recommend
@recommend.route("")
def index():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = dict(db_class.executeOne(search_user))

    return render_template('recommend/recommend.html', result=data)
  except Exception as e:
    print(e)
    return render_template('layout/error.html')

@recommend.route("/trend")
def trend():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "INSERT INTO search_log(s_type,user_id) VALUES ('tn','" + userid + "');"
    
    db_class.execute(search_user)
    db_class.commit()

    return render_template('recommend/trend.html')
  except Exception as e:
    print(e)
    return render_template('layout/error.html')

@recommend.route("/clothe")
def clothe():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "INSERT INTO search_log(s_type,user_id) VALUES ('co','" + userid + "');"
    
    db_class.execute(search_user)
    db_class.commit()

    return render_template('recommend/clothe.html')
  except Exception as e:
    print(e)
    return render_template('layout/error.html')
  
@recommend.route("/crawling")
def crawling():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "INSERT INTO search_log(s_type,user_id) VALUES ('cl','" + userid + "');"
    
    db_class.execute(search_user)
    db_class.commit()

    return render_template('recommend/crawling.html')
  except Exception as e:
    print(e)
    return render_template('layout/error.html')
  
@recommend.route("/statistic")
def statistic():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "INSERT INTO search_log(s_type,user_id) VALUES ('st','" + userid + "');"
    
    db_class.execute(search_user)
    db_class.commit()

    return render_template('recommend/statistic.html')
  except Exception as e:
    print(e)
    return render_template('layout/error.html')

