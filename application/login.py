from flask import Flask, render_template, session, redirect, request, url_for
from flask import Blueprint
import hashlib
# import dbModule
from application import dbModule

login = Blueprint("login", __name__, url_prefix="/login")

# Login
@login.route("")
def index():
  return render_template('user/login.html')

@login.route('/login',methods=['POST'])
def login_session():
  
  try:
    userid = request.form.get('userid')
    password = request.form.get('password')

    HASH_NAME = "md5"
    text = password.encode('utf-8')
    md5 = hashlib.new(HASH_NAME)
    md5.update(text)
    password_hash = md5.hexdigest()

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    db_result = db_class.executeOne(search_user)
    
    if db_result is None:
      # 쿼리 데이터가 없으면 출력
      result = '존재하지 않는 아이디 입니다.'
    else:
      data = dict(db_result)
      if data['pw'] == password_hash:
        # 로그인 처리
        session['user_Nm'] = data['userNm']
        session['user_id'] = data['id']
        session['login'] = True
        print('로그인 성공')
        return {
          'code':20000
        }
      else:
        # 비밀번호 틀림
        result = '비밀번호가 다릅니다.'
    
    return {
      'code':50000,
      'result': result
    }
  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }

@login.route('/logout', methods=['GET'])
def logout_session():
  session.pop('login', False)
  session.pop('user_Nm', None)
  session.pop('user_id', None)
  return redirect('/')