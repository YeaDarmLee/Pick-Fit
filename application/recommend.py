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

# @recommend.route("/trend")
# def trend():
#   try:
#     userid = '%s' % escape(session['user_id'])

#     db_class = dbModule.Database()
#     search_user = "INSERT INTO search_log(s_type,user_id) VALUES ('tn','" + userid + "');"

#     db_class.execute(search_user)
#     db_class.commit()

#     return render_template('recommend/trend.html')
#   except Exception as e:
#     print(e)
#     return render_template('layout/error.html')


@recommend.route("/clothe")
def clothe():
  try:
    userid = '%s' % escape(session['user_id'])
    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    user_data = dict(db_class.executeOne(search_user))

    age = user_data['age']
    gender = user_data['gender']
    height = user_data['height']
    weight = user_data['weight']
    face_shape = user_data['face_shape']
    body_shape = user_data['body_shape']
    style = user_data['style']
    skin_tone = user_data['skin_tone']
    hair = user_data['hair']

    if style == 1:
      print('클래식')
      style_sql = "WHERE style = '클래식' OR style_sub = '클래식'"
    elif style == 2:
      print('캐주얼')
      style_sql = "WHERE style = '캐주얼' OR style_sub = '캐주얼'"
    elif style == 3:
      print('매니시')
      style_sql = "WHERE style = '매니시' OR style_sub = '매니시'"
    elif style == 4:
      print('애스닉')
      style_sql = "WHERE style = '애스닉' OR style_sub = '애스닉'"
    elif style == 5:
      print('모던')
      style_sql = "WHERE style = '모던' OR style_sub = '모던'"
    elif style == 6:
      print('내추럴')
      style_sql = "WHERE style = '내추럴' OR style_sub = '내추럴'"
    elif style == 7:
      print('스포티')
      style_sql = "WHERE style = '스포티' OR style_sub = '스포티'"
    elif style == 8:
      print('힙합')
      style_sql = "WHERE style = '힙합' OR style_sub = '힙합'"
    
    # 키에따른 조건 필요 (패턴, 길이)
    if float(height) <= 140:
      height_sql = " AND length NOT IN ('롱')"
    elif float(height) <= 150:
      height_sql = " AND length NOT IN ('롱')"
    elif float(height) <= 160:
      height_sql = ""
    elif float(height) <= 170:
      height_sql = ""
    elif float(height) <= 180:
      height_sql = ""
    elif float(height) > 180:
      height_sql = ""

    bmi = float(weight) / ((float(height)/100) * (float(height)/100))
    if bmi <= 18.5:
      print('저체중')
      bmi_sql = " AND sleeve NOT IN ('민소매')"
    elif bmi <= 22.9:
      print('정상')
      bmi_sql = ""
    elif bmi <= 24.9:
      print('과체중')
      bmi_sql = " AND fit NOT IN ('타이트')"
    elif bmi > 25:
      print('비만')
      bmi_sql = " AND fit NOT IN ('스키니','타이트') AND sleeve NOT IN ('민소매')"

    # 얼굴형에 따른 넥라인 정의
    if face_shape == 1:
      print('달걀형')
      face_shape_sql = ""
    elif face_shape == 2:
      print('역삼각형')
      face_shape_sql = " AND neckline REGEXP '유넥|오프숄더|원숄더|스퀘어넥|후드|터틀넥|보트넥|스위트하트|0'"
    elif face_shape == 3:
      print('둥근형')
      face_shape_sql = " AND neckline REGEXP '브이넥|홀터넥|오프숄더|원숄더|스퀘어넥|노카라|스위트하트|0'"
    elif face_shape == 4:
      print('각진형')
      face_shape_sql = " AND neckline REGEXP '유넥|홀터넥|노카라|후드|스위트하트|0'"
    elif face_shape == 5:
      print('긴 얼굴형')
      face_shape_sql = " AND neckline REGEXP '유넥|홀터넥|후드|터틀넥|보트넥|0'"
    
    # 체형에 따른 넥라인 정의 및 추가조건 필요
    if body_shape == 1:
      print('모래시계형')
      body_shape_sql = ""
    elif body_shape == 2:
      print('직사각형')
      body_shape_sql = ""
    elif body_shape == 3:
      print('삼각형')
      body_shape_sql = ""
    elif body_shape == 4:
      print('역삼각형')
      body_shape_sql = ""
    elif body_shape == 5:
      print('타원형')
      body_shape_sql = ""

    query = "SELECT * FROM clothing_data " + style_sql + bmi_sql + face_shape_sql + height_sql + " order by rand() limit 50;"

    db_class = dbModule.Database()
    result = db_class.executeAll(query)

    img_array = []
    for i in result:
      img_binary = i['img']
      img_binary = img_binary.decode('UTF-8')
      img_array.append(img_binary)
    
    search_log = "INSERT INTO search_log(s_type,user_id,result) VALUES ('co','" + userid + "','미정');"
    db_class.execute(search_log)
    db_class.commit()

    return render_template('recommend/clothe.html', user = user_data, result = img_array)
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

