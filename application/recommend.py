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
    
    if gender == 0:
      # 남자
      gender_sql = " AND gender = 1"
    if gender == 1:
      # 여자
      gender_sql = " AND gender = 0"

    if style == 1:
      style = '로맨틱'
      style_sql = " AND style = '로맨틱'"
    elif style == 2:
      if gender == 0:
        style = '모던'
        style_sql = " AND style = '모던'"
      if gender == 1:
        style = '모던'
        style_sql = " AND style = '모던'"
    elif style == 3:
      if gender == 0:
        style = '스포티'
        style_sql = " AND style = '스포티'"
      if gender == 1:
        style = '스포티'
        style_sql = " AND style = '스포티'"
    elif style == 4:
      style = '클래식'
      style_sql = " AND style = '클래식'"
    elif style == 5:
      if gender == 0:
        style = '스트리트'
        style_sql = " AND style = '스트리트'"
      if gender == 1:
        style = '스트리트'
        style_sql = " AND style = '스트리트'"
    elif style == 6:
      style = '캐주얼'
      style_sql = " AND style = '캐주얼'"
    elif style == 7:
      style = '밀리터리'
      style_sql = " AND style = '밀리터리'"
    
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

    # 성별에 따른 img 조건
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
      face_shape_sql = " AND neckline REGEXP '유넥|홀터넥|노카라|오프숄더|원숄더|후드|스위트하트|0'"
    elif face_shape == 5:
      print('긴 얼굴형')
      face_shape_sql = " AND neckline REGEXP '홀터넥|후드|터틀넥|보트넥|0'"
    
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

    query = "SELECT * FROM clothing_data WHERE 1=1" + gender_sql + style_sql + bmi_sql + face_shape_sql + height_sql + " order by rand() limit 9;"
    print(query)
    db_class = dbModule.Database()
    result = db_class.executeAll(query)

    img_array = []
    for i in result:
      img_binary = i['img']
      img_binary = img_binary.decode('UTF-8')

      detailData = {
        "img_binary" : img_binary,
        "name" : i['shop'],
        "price" : format(int(i['price']), ','),
        "url" : i['url'],
        "p_name" : i['p_name']
      }

      img_array.append(detailData)
    
    search_log = "INSERT INTO search_log(s_type,user_id,result) VALUES ('co','" + userid + "','" + style + "');"
    db_class.execute(search_log)
    db_class.commit()

    return render_template('recommend/clothe.html', user = user_data, img_result = img_array)
  except Exception as e:
    print(e)
    return render_template('layout/error.html')
  
# @recommend.route("/crawling")
# def crawling():
#   return render_template('recommend/crawling.html')
  
# @recommend.route("/crawling_search",methods=['POST'])
# def crawling_search():
#   try:
#     searchUrl = request.form.get('searchUrl')
#     tag = request.form.get('tag')

#     if searchUrl == '' and tag == '':
#       return {
#         'code':50000,
#         'result': '모든 값을 입력해 주세요.'
#       }
#     elif searchUrl == '':
#       return {
#         'code':50000,
#         'result': '검색할 url을 입력해 주세요.'
#       }

#     # 크롤링 url 기본값
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
#     response = requests.get(searchUrl, headers=headers)
#     html_text = response.text
#     soup = BeautifulSoup(html_text, "lxml")
#     result = soup.find(tag).text

#     userid = '%s' % escape(session['user_id'])
    
#     cl_result = []
#     cl_result.append({
#         'searchUrl':searchUrl,
#         'tag':tag
#       })

#     db_class = dbModule.Database()
#     search_log = "INSERT INTO search_log(s_type,user_id,result) VALUES ('cl','" + userid + "','" + json.dumps(cl_result[0]) + "');"
#     db_class.execute(search_log)
#     db_class.commit()

#     return {
#         'code':20000,
#         'result': result,
#         'searchUrl': searchUrl,
#         'tag': tag,
#       }
#   except Exception as e:
#     print(e)
#     return {
#         'code':50000,
#         'result' : '크롤링에 실패하였습니다.<br>' + e
#       }
  
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

@recommend.route("/trend")
def trend():
  try:
    # recommend_c
    db_class = dbModule.Database()
    recommend_c_sql = "SELECT * FROM recommend_c;"
    recommend_c_data = db_class.executeAll(recommend_c_sql)

    return render_template('recommend/trend.html', list = recommend_c_data)
  except Exception as e:
    print(e)
    return render_template('layout/error.html')


@recommend.route("/addCombination", methods=['POST'])
def addCombination():
  try:
    title = request.form.get('title')
    outer = request.form.get('outer')
    top = request.form.get('top')
    bottom = request.form.get('bottom')
    notice = request.form.get('notice')

    if title == '':
      return {
        'code':50000,
        'msg': '제목을 입력해주세요.'
      }
    if notice == '':
      return {
        'code':50000,
        'msg': '상세설명을 입력해주세요'
      }
    else:
      notice = notice.replace("\r\n","<br>")
    
    if top == '' or bottom == '':
      return {
        'code':50000,
        'msg': '상의와 하의는 필수값입니다.'
      }

    userid = '%s' % escape(session['user_id'])
    
    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info WHERE id = '" + userid + "'"
    userData = db_class.executeOne(search_user)
    userNm = userData['userNm']
    
    search_user = "INSERT INTO recommend_c(title,detail,c_outer,top,bottom,user,userid) VALUES ('" + title + "','" + notice + "','" + outer + "','" + top + "','" + bottom + "','" + userNm + "','" + userid+ "');"

    db_class.execute(search_user)
    db_class.commit()

    return {
        'code':20000,
        'msg': "등록에 성공하였습니다."
      }
  except Exception as e:
    print(e)
    return {
        'code':50000,
        'msg': "등록에 실패하였습니다."
      }
  

@recommend.route("/t_detail")
def t_detail():
  try:
    idx = request.args.get('idx')

    db_class = dbModule.Database()
    search_data_sql = "SELECT * FROM recommend_c WHERE idx = '" + idx + "'"
    data = dict(db_class.executeOne(search_data_sql))

    c_date = data['date'].strftime('%Y-%m-%d'),

    user = data['userid']
    search_user_sql = "SELECT * FROM user_info WHERE id = '" + user + "'"
    user_data = dict(db_class.executeOne(search_user_sql))

    c_outer = data['c_outer']
    if c_outer != '':
      search_clothing_data_c_outer_sql = "SELECT * FROM clothing_data WHERE idx = '" + c_outer + "'"
      c_outer_data = dict(db_class.executeOne(search_clothing_data_c_outer_sql))
      c_outer_img_binary = c_outer_data['img']
      c_outer_img_binary = c_outer_img_binary.decode('UTF-8')
      c_outerData = {
          "shop" : c_outer_data['shop'],
          "price" : format(int(c_outer_data['price']), ','),
          "p_name" : c_outer_data['p_name'],
          "url" : c_outer_data['url'],
          "img_binary" : c_outer_img_binary
        }
    else:
      c_outerData = {
          "shop" : 0,
          "price" : 0,
          "p_name" : 0,
          "img_binary" : 0
        }

    top = data['top']
    search_clothing_data_top_sql = "SELECT * FROM clothing_data WHERE idx = '" + top + "'"
    top_data = dict(db_class.executeOne(search_clothing_data_top_sql))
    top_img_binary = top_data['img']
    top_img_binary = top_img_binary.decode('UTF-8')
    topData = {
        "shop" : top_data['shop'],
        "price" : format(int(top_data['price']), ','),
        "p_name" : top_data['p_name'],
        "url" : top_data['url'],
        "img_binary" : top_img_binary
      }

    bottom = data['bottom']
    search_clothing_data_bottom_sql = "SELECT * FROM clothing_data WHERE idx = '" + bottom + "'"
    bottom_data = dict(db_class.executeOne(search_clothing_data_bottom_sql))
    bottom_img_binary = bottom_data['img']
    bottom_img_binary = bottom_img_binary.decode('UTF-8')
    bottomData = {
        "shop" : bottom_data['shop'],
        "price" : format(int(bottom_data['price']), ','),
        "p_name" : bottom_data['p_name'],
        "url" : bottom_data['url'],
        "img_binary" : bottom_img_binary
      }

    return render_template('recommend/t_detail.html', result = data, user_data = user_data, c_outerData = c_outerData, topData = topData, bottomData = bottomData, c_date = c_date[0], idx = idx)
  except Exception as e:
    print(e)
    return render_template('layout/error.html')

@recommend.route("/search_outer", methods=['POST'])
def search_outer():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = dict(db_class.executeOne(search_user))
    
    # 남자
    if data['gender'] == 0:
      gender = "1"
    else:
      gender = "0"

    db_class = dbModule.Database()
    search_outer_sql = "SELECT * FROM clothing_data WHERE title = '아우터' AND gender = " + gender
    data = db_class.executeAll(search_outer_sql)
  
    results = []
    for i in data:
      detail_data = []
      detail_data = dict(i)

      img_binary = detail_data['img']
      img_binary = img_binary.decode('UTF-8')

      detailData = {
        "idx" : detail_data['idx'],
        "img_binary" : img_binary,
      }
      
      results.append(detailData)

    return {
        'code':20000,
        'results': results
      }
  except Exception as e:
    print(e)

@recommend.route("/search_top", methods=['POST'])
def search_top():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = dict(db_class.executeOne(search_user))
    
    # 남자
    if data['gender'] == 0:
      gender = "1"
    else:
      gender = "0"

    db_class = dbModule.Database()
    search_top_sql = "SELECT * FROM clothing_data WHERE title = '상의' AND gender = " + gender
    data = db_class.executeAll(search_top_sql)
  
    results = []
    for i in data:
      detail_data = []
      detail_data = dict(i)

      img_binary = detail_data['img']
      img_binary = img_binary.decode('UTF-8')

      detailData = {
        "idx" : detail_data['idx'],
        "img_binary" : img_binary,
      }
      
      results.append(detailData)

    return {
        'code':20000,
        'results': results
      }
  except Exception as e:
    print(e)

@recommend.route("/search_bottom", methods=['POST'])
def search_bottom():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = dict(db_class.executeOne(search_user))
    
    # 남자
    if data['gender'] == 0:
      gender = "1"
    else:
      gender = "0"

    db_class = dbModule.Database()
    search_bottom_sql = "SELECT * FROM clothing_data WHERE title = '하의' AND gender = " + gender
    data = db_class.executeAll(search_bottom_sql)
    
    results = []
    for i in data:
      try:
        detail_data = []
        detail_data = dict(i)

        img_binary = detail_data['img']
        img_binary = img_binary.decode('UTF-8')

        detailData = {
          "idx" : detail_data['idx'],
          "img_binary" : img_binary,
        }
        
        results.append(detailData)

      except Exception as e:
        print(0)
      
    return {
        'code':20000,
        'results': results
      }
  except Exception as e:
    print(e)
    