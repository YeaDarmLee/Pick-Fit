# /app.py
from os import error
from flask import Flask, render_template, request
from urllib import parse

# dbModule.py import
import dbModule

# 크롤링 라이브러리 import
import requests 
from bs4 import BeautifulSoup

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
    # soup.select_one('//*[@id="tt-body-page"]/script[2]')
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
  except Exception as e:
    print(e)
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
  print(rq_form)

  hostName = request.form.get('hostName')
  url = request.form.get('url')
  detail_url = request.form.get('detail_url')
  
  url = parse.unquote(url)
  detail_url = parse.unquote(detail_url)

  price = request.form.get('price')
  p_name = request.form.get('p_name')
  width = request.form.get('width')
  flexibility = request.form.get('flexibility')
  seethrough = request.form.get('seethrough')
  lining = request.form.get('lining')
  material = request.form.get('material')
  p_img = request.form.get('p_img')
  size = request.form.get('size')
  color = request.form.get('color')

  try:
    db_class = dbModule.Database()

    # 현재 두 테이블간 의존성이 없이 동시에 insert하고 있어 둘중 하나가 에러나면 idx 번호 꼬임
    # 이문제 처리해야하는데 귀찬음...

    # url_info insert
    sql_url_info = "INSERT INTO url_info (hostName,url,detail_url) VALUES ('" + hostName + "','" + str(url) + "',\"" + str(detail_url) + "\")"
    print(sql_url_info)
    db_class.execute(sql_url_info)

    # product_info insert
    sql_product_info = "INSERT INTO product_info (price,p_name,width,flexibility,seethrough,lining,material,p_img,size,color) VALUES ('" + str(price) + "','" + str(p_name) + "','" + str(width) + "','" + str(flexibility) + "','" + str(seethrough) + "','" + str(lining) + "','" + str(material) + "','" + str(p_img) + "','" + str(size) + "','" + str(color) + "')"
    print(sql_product_info)
    db_class.execute(sql_product_info)

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
  search_url_info = "SELECT * FROM url_info;"
  url_info_result = db_class.executeAll(search_url_info)

  result = []
  for i in url_info_result:
    result.append(i)

  return {'result': result}


@app.route('/crawling',methods=('GET', 'POST'))
def crawling():
  from selenium import webdriver
  from webdriver_manager.chrome import ChromeDriverManager

  options = webdriver.ChromeOptions()
  options.add_argument('headless')
  options.add_argument('window-size=1920x1080')
  options.add_argument("disable-gpu")

  # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

  driver.get('https://mr-s.co.kr/product/detail.html?product_no=40244')
  driver.implicitly_wait(2)
  # driver.get_screenshot_as_file('test.png')

  print('find_elements_by_xpath : ',[e.text for e in driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[4]/div[1]/div/center[2]/div[1]/div[2]/div[2]/div[2]')])

  
  driver.close()

  return render_template("crawling.html", result = result)



########## test ##########

# test code
@app.route('/test',methods=('GET', 'POST'))
def test():
  from selenium import webdriver
  from webdriver_manager.chrome import ChromeDriverManager

  options = webdriver.ChromeOptions()
  options.add_argument('headless')
  options.add_argument("disable-gpu")

  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

  driver.get('https://mr-s.co.kr/product/detail.html?product_no=40244')
  driver.implicitly_wait(2)

  print('find_elements_by_xpath : ',[e.text for e in driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[4]/div[1]/div/center[2]/div[1]/div[2]/div[2]/div[2]')])

  
  driver.close()

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