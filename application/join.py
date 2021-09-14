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

    # 비밀번호 해쉬화
    HASH_NAME = "md5"
    text = password.encode('utf-8')
    md5 = hashlib.new(HASH_NAME)
    md5.update(text)
    password_hash = md5.hexdigest()

    db_class = dbModule.Database()
    search_user = "INSERT INTO user_test(id,pw,userNm) VALUES ('" + userid + "','" + password_hash + "','" + userNm + "')"

    db_class.execute(search_user)
    db_class.commit()
    print('회원가입 성공')
    return redirect('/index')
  except Exception as e:
    print(e)
    return {'result': e}

