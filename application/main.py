from flask import Flask, render_template, request, redirect, escape, session
from flask import Blueprint

# import dbModule
from application import dbModule

main = Blueprint("main", __name__, url_prefix="/")

@main.route("")
@main.route("/index")
def index():
  return render_template('index.html')

@main.route("/myPage")
def myPage():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    user_data = dict(db_class.executeOne(search_user))
    
    search_log = "SELECT * FROM search_log where user_id = '" + userid + "' ORDER BY c_date DESC limit 100;"
    log_data = db_class.executeAll(search_log)

    results = []
    for x in log_data:
      s_type = ''
      detail_data = []
      detail_data = dict(x)
      if detail_data['s_type'] == 'tn':
        s_type = '트렌드 조회'
      elif detail_data['s_type'] == 'co':
        s_type = '의류 추천'
      elif detail_data['s_type'] == 'cl':
        s_type = '크롤링'
      elif detail_data['s_type'] == 'st':
        s_type = '통계 조회'
      
      results.append({
        'idx':detail_data['idx'],
        's_type':s_type,
        'user_id':detail_data['user_id'],
        'date':detail_data['c_date']
      })

    return render_template('user/myPage.html', user=user_data, log=results)

  except Exception as e:
    print(e)
    return render_template('layout/error.html')
