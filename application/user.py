from flask import Flask, render_template, session, redirect, request, url_for, escape
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

    print(userid)

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info WHERE id = '" + userid + "';"
    print(search_user)
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
    age = request.form.get('age')
    gender = request.form.get('gender')
    height = request.form.get('height')
    weight = request.form.get('weight')

    print(gender)

    if userNm == '' or userid == '' or password == '' or age == '' or gender == '성별을 선택해 주세요' or height == '' or weight == '':
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
      search_user = "INSERT INTO user_info(id,pw,userNm,age,gender,height,weight) VALUES ('" + userid + "','" + password_hash + "','" + userNm + "','" + age + "','" + gender + "','" + height + "','" + weight + "')"

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

# 비밀번호 변경
@user.route('/change_pw',methods=['POST'])
def change_pw():
  try:
    current_pw = request.form.get('current_pw')
    new_pw = request.form.get('new_pw')
    newCheck_pw = request.form.get('newCheck_pw')

    if current_pw == '' or new_pw == '' or newCheck_pw == '':
      return {
        'code':50000,
        'result': '모든 값을 입력해 주세요.'
      }
    elif new_pw != newCheck_pw:
      return {
        'code':50000,
        'result': '새 비밀번호가 서로 다릅니다.'
      }

    # 비밀번호 해쉬화
    HASH_NAME = "md5"
    new_pw_text = new_pw.encode('utf-8')
    md5 = hashlib.new(HASH_NAME)
    md5.update(new_pw_text)
    new_pw_hash = md5.hexdigest()

    current_pw_text = current_pw.encode('utf-8')
    md5 = hashlib.new(HASH_NAME)
    md5.update(current_pw_text)
    current_pw_hash = md5.hexdigest()

    # 세션에 있는 user id로 db 조회
    userid = '%s' % escape(session['user_id'])
    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = db_class.executeOne(search_user)

    if data['pw'] == current_pw_hash:
      current_pw_sql = 'UPDATE user_info SET pw = "' + new_pw_hash + '" WHERE id = "' + userid + '";'
      db_class.execute(current_pw_sql)
      db_class.commit()

      return {
        'code':20000,
        'result': '비밀번호 변경이 완료되었습니다.'
      }

    else:
      return {
        'code':50000,
        'result': '현재 비밀번호가 다릅니다.'
      }

  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }

# 회원탈퇴
@user.route('/secession',methods=['POST'])
def secession():
  try:
    # 세션에 있는 user id로 db 조회
    userid = '%s' % escape(session['user_id'])
    db_class = dbModule.Database()
    sql = "DELETE FROM user_info WHERE id='" + userid + "';"

    db_class.execute(sql)
    db_class.commit()

    # 세션 초기화
    session.pop('login', False)
    session.pop('user_Nm', None)
    session.pop('user_id', None)

    return {
        'code':20000,
        'result': '회원탈퇴가 완료 되었습니다.'
      }

  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }

# 수정하기 modify
@user.route('/modify',methods=['POST'])
def modify():
  try:
    body_shape = request.form.get('body_shape')
    style = request.form.get('style')
    skin_tone = request.form.get('skin_tone')
    face_shape = request.form.get('face_shape')
    hair = request.form.get('hair')

    query = ''
    if body_shape != None:
      query += 'body_shape = "' + body_shape + '",'
    if style != None:
      query += 'style = "' + style + '",'
    if skin_tone != None:
      query += 'skin_tone = "' + skin_tone + '",'
    if face_shape != None:
      query += 'face_shape = "' + face_shape + '",'
    if hair != None:
      query += 'hair = "' + hair + '",'

    # 세션에 있는 user id로 db 조회
    userid = '%s' % escape(session['user_id'])
    db_class = dbModule.Database()
    sql = "UPDATE user_info SET " + query[0:len(query)-1] + " WHERE id='" + userid + "';"
    
    db_class.execute(sql)
    db_class.commit()

    return {
      'code':20000,
      'result': '업데이트가 완료되었습니다.'
    }

  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }