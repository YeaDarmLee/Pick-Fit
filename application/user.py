from flask import Flask, render_template, session, redirect, request, url_for
from flask import Blueprint
import hashlib
# import dbModule
from application import dbModule

user = Blueprint("user", __name__, url_prefix="/user")

# Login
@user.route("/login")
def login():
  return render_template('user/login.html')

@user.route('/logout', methods=['GET'])
def logout():
  session.pop('login', False)
  session.pop('user_Nm', None)
  session.pop('user_id', None)
  return redirect('/')

@user.route('/examine',methods=['POST'])
def examine():
  
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


# join
@user.route("/join")
def join():
  return render_template('user/join.html')


@user.route('/register',methods=['POST'])
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
      search_user = "INSERT INTO user_info(id,pw,userNm,gender,height,weight) VALUES ('" + userid + "','" + password_hash + "','" + userNm + "','" + gender + "','" + height + "','" + weight + "')"

      db_class.execute(search_user)
      db_class.commit()
      
      print('회원가입 성공')

      return {
        'code':20000,
        'result': '회원가입에 성공하였습니다.'
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

