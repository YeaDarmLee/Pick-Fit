from flask import Flask, render_template, request, escape, session
from flask import Blueprint
import json
# import dbModule
from application import dbModule
# 크롤링 라이브러리 import
import requests 
from bs4 import BeautifulSoup

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
  return render_template('recommend/crawling.html')
  
@recommend.route("/crawling_search",methods=['POST'])
def crawling_search():
  try:
    searchUrl = request.form.get('searchUrl')
    tag = request.form.get('tag')

    # 크롤링 url 기본값
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(searchUrl, headers=headers)
    html_text = response.text
    soup = BeautifulSoup(html_text, "lxml")
    result = soup.find(tag).text

    userid = '%s' % escape(session['user_id'])
    
    cl_result = []
    cl_result.append({
        'searchUrl':searchUrl,
        'tag':tag
      })

    db_class = dbModule.Database()
    search_log = "INSERT INTO search_log(s_type,user_id,result) VALUES ('cl','" + userid + "','" + json.dumps(cl_result[0]) + "');"
    db_class.execute(search_log)
    db_class.commit()

    return {
        'code':20000,
        'result': result,
        'searchUrl': searchUrl,
        'tag': tag,
      }
  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result' : '크롤링에 실패하였습니다.'
      }
  
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

