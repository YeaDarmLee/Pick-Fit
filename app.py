# /app.py
from flask import Flask, render_template, request
app = Flask(__name__)

# 크롤링 라이브러리 import
import requests 
from bs4 import BeautifulSoup

@app.route('/')
def hello():
  return render_template('index.html')


@app.route('/getPostTest',methods=('GET', 'POST'))
def index():
  
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')
  message = request.form.get('message')
  data = {'name': name, 'email': email, 'phone': phone, 'message': message}

  return render_template('getPostTest.html', data = data)

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
    response = requests.get(url)
    html_text = response.text
    soup = BeautifulSoup(html_text, "lxml")

    result_txt = []
    result_img = []
    # 크롤링
    # soup.find("tag",class_="name").get_text()
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
      "url": url,
      "tag": '',
      "classNm": '',
      'result_img': '',
      'result_txt': ''
    }
  
  return render_template("crawler.html", result = result)

if __name__=="__main__":
    app.run(host="127.0.0.1", port="8888", debug=True)