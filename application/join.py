from flask import Flask, render_template, request, redirect
from flask import Blueprint
import hashlib
# import dbModule
from application import dbModule

join = Blueprint("join", __name__, url_prefix="/join")

# Join
@join.route("")
def index():
  return render_template('user/join.html')

@join.route('/register',methods=['POST'])
def register():
  try:
    # 기존 user id 체크
    userNm = request.form.get('userNm')
    userid = request.form.get('userid')
    password = request.form.get('password')
    gender = request.form.get('gender')
    height = request.form.get('height')
    weight = request.form.get('weight')

    print(gender)

    if userNm == '' or userid == '' or password == '' or gender == '성별을 선택해 주세요' or height == '' or weight == '':
      return {
        'code':50000,
        'result': '모든 값을 입력해 주세요.'
      }

    # 비밀번호 해쉬화
    HASH_NAME = "md5"
    text = password.encode('utf-8')
    md5 = hashlib.new(HASH_NAME)
    md5.update(text)
    password_hash = md5.hexdigest()

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = db_class.executeOne(search_user)

    if data is None:
      db_class = dbModule.Database()
      search_user = "INSERT INTO user_info(id,pw,userNm,gender,height,weight) VALUES ('" + userid + "','" + password_hash + "','" + userNm + "','" + gender + "','" + height + "','" + weight + "')"

      db_class.execute(search_user)
      db_class.commit()
      
      print('회원가입 성공')

      return {
        'code':20000
      }
    else:
      return {
        'code':50000,
        'result': '이미 가입되어 있는 아이디 입니다.'
      }
  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }

