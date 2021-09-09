# /app.py
from flask import Flask, render_template, request
app = Flask(__name__)

# 크롤링 라이브러리 import
import requests 
from bs4 import BeautifulSoup 
import unicodedata

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

@app.route('/crawler',methods=('GET', 'POST'))
def crawler():
  response = ''
  html_text = ''
  soup = ''
  title = ''

  url = request.form.get('url')
  tag = request.form.get('tag')

  if tag is None:
    tag = 'div'
  
  print(tag)

  if url is not None:
    try :
      response = requests.get(url)
      html_text = response.text
      
      soup = BeautifulSoup(html_text, "lxml") 
      title = soup.find("h1").get_text()
      
      content = soup.find(tag).get_text()
      content = unicodedata.normalize("NFKD", content)
    except :
      title = '검색하는 페이지에 설정한 태그가 없습니다.'
      content = 'Error : 이 에러가 보이면 해당 URL, 혹은 html 구조를 확인해 보세요.'
      url = url
  else:
    title = ''
    content = ''
    url = ''
  
  return render_template("crawler.html", list = title, content = content, tag = tag, url = url)

if __name__=="__main__":
    app.run(host="127.0.0.1", port="8888", debug=True)