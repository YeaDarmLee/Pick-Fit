# /app.py
from os import error
from flask import Flask, render_template, request
import dbModule

# 크롤링 라이브러리 import
import requests 
from bs4 import BeautifulSoup

from urllib import parse

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

# 
# 크롤링 route
# 상태코드값 추가
# 20000 = success / 40000 = fail / 50000 = 초기 로딩
# 
@app.route('/crawler',methods=('GET', 'POST'))
def crawler():
  try:
    # front에서 넘겨받은 form값
    rq_form = request.form

    # 초기 로딩 시 url이 없어 에러뜨는 거 방지용 바로 return
    if (len(rq_form) == 0):
      result = {
        "code": 50000,
        "url": '',
        "tag": '',
        "classNm": '',
        'result_img': '',
        'result_txt': ''
      }
      return render_template("crawler.html", result = result)

    j = 0
    tag = []
    classNm = []
    # 크롤링에 필요한 tag와 class 값 분할
    for i in rq_form:
      if (j == 0):
        url = request.form.get(i)
      elif (j != 0 and j%2 == 0):
        classNm.append(request.form.get(i))
      else:
        tag.append(request.form.get(i))
      j=j+1

    # 크롤링 url 기본값
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html_text = response.text
    soup = BeautifulSoup(html_text, "lxml")

    result_txt = []
    result_img = []
    # 크롤링
    # soup.select_one('#s_content > div.section > ul > li:nth-child(1) > dl > dt > a')
    for k in range(0, len(tag)):
      # 태그 Null 값 제외
      if (tag[k] != ''):
        # 이미지 태그 Search
        if (tag[k] == 'img'):
          if (classNm[k] == ''):
            img = soup.find(tag[k])
          else:
            img = soup.find(tag[k],class_=classNm[k])
          result_img.append(img.get("src"))
        # 일반 태그 Search
        else:
          if (classNm[k] == ''):
            result_txt.append(soup.find(tag[k]).get_text())
          else:
            result_txt.append(soup.find(tag[k],class_=classNm[k]).get_text())
    
    # return 형식 저장
    result = {
      "code": 20000,
      "url": url,
      "tag": tag,
      "classNm": classNm,
      'result_img': result_img,
      'result_txt': result_txt
    }
  except:
    result = {
      "code": 40000,
      "url": '',
      "tag": '',
      "classNm": '',
      'result_img': '',
      'result_txt': ''
    }
  
  return render_template("crawler.html", result = result)

# DB에 크롤링 양식 저장
@app.route('/addTemplate',methods=('GET', 'POST'))
def addTample():
  # front에서 넘겨받은 form값
  rq_form = request.form

  tampleName = request.form.get('tampleName')
  tampleUrl = request.form.get('tampleUrl')
  
  # URL 입력시 자동 인코딩으로 인한 TypeError로 디코딩 처리
  tampleUrl = parse.unquote(tampleUrl)

  j = 0
  tag = []
  classNm = []
  # 크롤링에 필요한 tag와 class 값 분할
  for i in rq_form:
    if (i != 'tampleName' and i != 'tampleUrl'):
      if (j != 0 and j%2 == 0):
        tag.append(request.form.get(i))
      else:
        classNm.append(request.form.get(i))
    j=j+1
  
  print('tag',tag)
  print('classNm',classNm)

  # data insert
  try:
    db_class = dbModule.Database()
    sql = "INSERT INTO crawling_form (title,url,meta_tag,meta_class) VALUES ('" + tampleName + "','" + str(tampleUrl) + "',\"" + str(tag) + "\",\"" + str(classNm) + "\")"
    print (sql)

    db_class.execute(sql)
    db_class.commit()
    result = {
      "code": 20000
    }
  except Exception as e:
    print(e)
    result = {
      "code": 50000,
      "error": e
    }

  return result

# searchTemplate
@app.route('/searchTemplate',methods=('GET', 'POST'))
def searchTample():

  db_class = dbModule.Database()
  sql = "SELECT * FROM crawling_form;"
  row = db_class.executeAll(sql)

  result = []
  for i in row:
    result.append(i)

  return {'result': result}



########## test ##########

# test code
@app.route('/test',methods=('GET', 'POST'))
def test():
  url = 'https://wjdqnwnd.cafe24.com/product/detail.html?product_no=7132&cate_no=99&display_group=1'
  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
  response = requests.get(url, headers=headers).text
  html_text = response
  soup = BeautifulSoup(html_text, "html.parser")
  print(soup)
  test = soup.find('h2')
  print(test)

  return 'test'

# databases test code
@app.route('/testdb')
def select():
    db_class = dbModule.Database()
    sql = "SELECT * FROM crawling_form;"
    row = db_class.executeAll(sql)
    print(row[0])

    return render_template('test.html', resultData=row)

########## test 모듈 ##########

if __name__=="__main__":
    app.run(host="127.0.0.1", port="8888", debug=True)

from app import app