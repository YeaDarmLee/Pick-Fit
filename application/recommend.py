from flask import Flask, render_template, request, escape, session
from flask import Blueprint
import json
# import dbModule
from application import dbModule
# 크롤링 라이브러리 import
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
    xpath = request.form.get('xpath')

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    driver.get(searchUrl)
    driver.implicitly_wait(2)

    xpath_result = [e.text for e in driver.find_elements_by_xpath(xpath)]
    print(xpath_result[0])
    print(driver.find_elements_by_xpath(xpath))

    userid = '%s' % escape(session['user_id'])
    
    cl_result = []
    cl_result.append({
        'searchUrl':searchUrl,
        'xpath':xpath
      })
      
    db_class = dbModule.Database()
    search_log = "INSERT INTO search_log(s_type,user_id,result) VALUES ('cl','" + userid + "','" + json.dumps(cl_result) + "');"
    db_class.execute(search_log)
    db_class.commit()

    return {
        'code':20000,
        'xpath_result': xpath_result,
        'searchUrl': searchUrl,
        'xpath': xpath,
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

