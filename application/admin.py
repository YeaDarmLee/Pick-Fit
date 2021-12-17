from flask import Flask, render_template, request, redirect, escape, session
from flask import Blueprint
import json

# import dbModule
from application import dbModule

# 이미지 관련
from werkzeug.utils import secure_filename
import io, base64
from PIL import Image

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("")
@admin.route("/index")
def index():
  return render_template('admin/index.html')

@admin.route('/fileUpload', methods = ['GET', 'POST'])
def fileUpload():
  try:
    files = request.files.getlist("file[]")
    for i in files:
      file_json = json.load(i)
      file_data = dict(file_json)

      print('#############  Json 업로드 시작  #############')

      labeling_data = file_data['데이터셋 정보']['데이터셋 상세설명']['라벨링']

      # file_name
      file_name = file_data['이미지 정보']['이미지 식별자']
      column = 'file_name'
      values = "'" + str(file_name) + ".jpg'"

      # title
      if (len(labeling_data['아우터'][0]) > 0) :
        title = '아우터'
        datail_data = labeling_data['아우터'][0]
      elif (len(labeling_data['원피스'][0]) > 0) :
        title = '원피스'
        datail_data = labeling_data['원피스'][0]
      elif (len(labeling_data['상의'][0]) > 0) :
        title = '상의'
        datail_data = labeling_data['상의'][0]
      elif (len(labeling_data['하의'][0]) > 0) :
        title = '하의'
        datail_data = labeling_data['하의'][0]
      
      column = column + ',title'
      values = values + ",'" + title + "'"

      # style
      if labeling_data['스타일'][0].get('스타일') is not None:
        style = labeling_data['스타일'][0]['스타일']
        column = column + ',style'
        values = values + ",'" + style + "'"

      # style_sub
      if labeling_data['스타일'][0].get('서브스타일') is not None:
        style_sub = labeling_data['스타일'][0]['서브스타일']
        column = column + ',style_sub'
        values = values + ",'" + style_sub + "'"

      # length
      if datail_data.get('기장') is not None:
        length = datail_data['기장']
        column = column + ',length'
        values = values + ",'" + length + "'"

      # color
      if datail_data.get('색상') is not None:
        color = datail_data['색상']
        column = column + ',color'
        values = values + ",'" + color + "'"

      # color_sub
      if datail_data.get('서브색상') is not None:
        color_sub = datail_data['서브색상']
        column = column + ',color_sub'
        values = values + ",'" + color_sub + "'"

      # category
      if datail_data.get('카테고리') is not None:
        category = datail_data['카테고리']
        column = column + ',category'
        values = values + ",'" + category + "'"

      # collar
      if datail_data.get('옷깃') is not None:
        collar = datail_data['옷깃']
        column = column + ',collar'
        values = values + ",'" + collar + "'"

      # sleeve
      if datail_data.get('소매기장') is not None:
        sleeve = datail_data['소매기장']
        column = column + ',sleeve'
        values = values + ",'" + sleeve + "'"

      # detail
      if datail_data.get('디테일') is not None:
        detail = ''
        for i in datail_data['디테일']:
          detail = detail + i +","
        column = column + ',detail'
        values = values + ",'" + detail[: - 1] + "'"

      # material
      if datail_data.get('소재') is not None:
        material = ''
        for i in datail_data['소재']:
          material = material + i +","
        column = column + ',material'
        values = values + ",'" + material[: - 1] + "'"
        
      # pattern
      if datail_data.get('프린트') is not None:
        pattern = ''
        for i in datail_data['프린트']:
          pattern = pattern + i +","
        column = column + ',pattern'
        values = values + ",'" + pattern[: - 1] + "'"

      # neckline
      if datail_data.get('넥라인') is not None:
        neckline = datail_data['넥라인']
        column = column + ',neckline'
        values = values + ",'" + neckline + "'"

      # fit
      if datail_data.get('핏') is not None:
        fit = datail_data['핏']
        column = column + ',fit'
        values = values + ",'" + fit + "'"

      # safe
      if datail_data.get('세이프') is not None:
        safe = datail_data['세이프']
        column = column + ',safe'
        values = values + ",'" + safe + "'"

      # silhouette
      if datail_data.get('실루엣') is not None:
        silhouette = datail_data['실루엣']
        column = column + ',silhouette'
        values = values + ",'" + silhouette + "'"
      
      if file_data['데이터셋 정보']['데이터셋 상세설명'].get('상세설명') is not None:
        detail_data = file_data['데이터셋 정보']['데이터셋 상세설명']['상세설명']
      else:
        detail_data = file_data['데이터셋 정보']['상세설명']

      column = column + ',shop,price,p_name,url'

      if detail_data.get('아우터') is not None:
        values = values + ",'" + detail_data['아우터'][0]['쇼핑몰'] + "'"
        values = values + ",'" + detail_data['아우터'][0]['가격'].replace(",","",2).replace("원","") + "'"
        values = values + ",'" + detail_data['아우터'][0]['상품명'] + "'"
        values = values + ",'" + detail_data['아우터'][0]['URL'] + "'"
      elif detail_data.get('원피스') is not None:
        values = values + ",'" + detail_data['원피스'][0]['쇼핑몰'] + "'"
        values = values + ",'" + detail_data['원피스'][0]['가격'].replace(",","",2).replace("원","") + "'"
        values = values + ",'" + detail_data['원피스'][0]['상품명'] + "'"
        values = values + ",'" + detail_data['원피스'][0]['URL'] + "'"
      elif detail_data.get('상의') is not None:
        values = values + ",'" + detail_data['상의'][0]['쇼핑몰'] + "'"
        values = values + ",'" + detail_data['상의'][0]['가격'].replace(",","",2).replace("원","") + "'"
        values = values + ",'" + detail_data['상의'][0]['상품명'] + "'"
        values = values + ",'" + detail_data['상의'][0]['URL'] + "'"
      elif detail_data.get('하의') is not None:
        values = values + ",'" + detail_data['하의'][0]['쇼핑몰'] + "'"
        values = values + ",'" + detail_data['하의'][0]['가격'].replace(",","",2).replace("원","") + "'"
        values = values + ",'" + detail_data['하의'][0]['상품명'] + "'"
        values = values + ",'" + detail_data['하의'][0]['URL'] + "'"
      
      # 남성 json 및 이미지 등록시 이 주석 풀고 업로드 해야함
      # column = column + ",gender"
      # values = values + ", '1'"

      sql = "INSERT clothing_data (" + column + ") VALUES (" + values + ")"

      try:
        db_class = dbModule.Database()
        db_class.execute(sql)
        db_class.commit()
      except Exception as e:
        print("###################################################################")
        print(file_data['이미지 정보']['이미지 식별자'])
        print("###################################################################")
      
      print('파일명 : ' , file_data['이미지 정보']['이미지 식별자'])
      print('###############  업로드 완료  ################')

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

@admin.route('/imgUpload', methods = ['GET', 'POST'])
def imgUpload():
  try:
    files = request.files.getlist("file[]")
    
    for i in files:
      data = i.read()

      binary = base64.b64encode(data)
      binary = binary.decode('UTF-8')

      db_class = dbModule.Database()
      sql = "UPDATE clothing_data SET img = '" + binary + "' WHERE file_name = '" + i.filename + "';"
      print(i.filename)
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