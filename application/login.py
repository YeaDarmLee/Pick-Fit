from flask import Flask, render_template, session, redirect, request, url_for
from flask import Blueprint
# import dbModule
from application import dbModule

login = Blueprint("login", __name__, url_prefix="/login")

# Login
@login.route("")
def index():
  # if session['login']:
  #   print('session[]OOOOOO')
  # else:
  #   print('session[]XXXXX')
  return render_template('user/login.html')

@login.route('/login',methods=['POST'])
def login_session():
  
  try:
    userid = request.form.get('userid')
    password = request.form.get('password')

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_test where id = '" + userid + "';"
    data = dict(db_class.executeOne(search_user))

    if data is not None:
      if data['pw'] == password:
        # 로그인 처리
        session['userid'] = userid
        session['login'] = True
        result = '로그인 성공'
      else:
        # 비밀번호 틀림
        result = 'PW가 다릅니다.'
    else:
      # 쿼리 데이터가 없으면 출력
      result = 'ID가 없는 사용자 입니다.'
    
    print(result)
    return redirect(url_for('/', result = result))

  except Exception as e:
    print(e)
    return {'result': e}

@login.route('/logout', methods=['GET'])
def logout_session():
  session.pop('userid', None)
  session.pop('login', False)
  return redirect('/')