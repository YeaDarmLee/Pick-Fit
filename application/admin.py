from flask import Flask, render_template, request, redirect, escape, session
from flask import Blueprint
import json

# import dbModule
from application import dbModule

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
      
      sql = "INSERT clothing_data (" + column + ") VALUES (" + values + ")"

      db_class = dbModule.Database()
      db_class.execute(sql)
      db_class.commit()
      
      print('values :::: ',values)

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