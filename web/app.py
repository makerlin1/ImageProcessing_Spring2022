# -*- coding: utf-8 -*-
from flask import Flask
from flask import url_for, escape, render_template, jsonify, send_from_directory
from flask import request
# 跨域
# from flask_cors import CORS

import requests, json
from werkzeug.utils import secure_filename
import os
import uuid
# 自定义函数
from utils import convert

# 全局变量
conf = {
    'site': {
        'name': '图像超分演示系统',
    },
    'tongji': {
        'viewer': 153,
        'task_start': 0,
        'task_end': 0,
        'speed': 0.012,
    }
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input/' #文件上传位置
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10 #100M, 上传的文件的最大大小（以字节为单位）

############################# 模板部分 #############################
# 模板上下文处理函数（类似全局变量）
@app.context_processor
def context_processor():  # 函数名可以随意修改
    return conf
# 异常处理
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码

# 首页 /
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

############################# 接口部分 #############################
# /api
# 统计数据
@app.route('/api/tongji')
def tongji():
    global conf
    if str(request.args.get('init')) == '1': conf['tongji']['viewer'] += 1 #pv加一
    
    ret = conf['tongji'].copy()
    ret['task_start'] += len(os.listdir('./input/'))
    ret['task_end'] += len(os.listdir('./output/'))
    ret['task_ing'] = ret['task_start'] - ret['task_end']
    return jsonify(ret)
# 文件上传
@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        taskId = uuid.uuid4().hex #随机uuid
        suffix = secure_filename(f.filename).split('.')[-1]
        filename = taskId + '.' + suffix
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        convert(filename) #转换utils.convert
        ret = {
            'status': 1,
            # 'taskId': taskId,
            'filename': filename,
            'tip': '上传成功！'
        }
        return jsonify(ret)
# 查询任务状态
@app.route('/api/query', methods=['GET'])
def query():
    if request.method == 'GET':
        filename = request.args.get('filename')
        ret = {
            'status': -1, #不存在-1, 转换中0, 转换成功1
            # 'taskId': taskId,
            'filename': '',
            'tip': '任务不存在'
        }
        if os.path.exists(f"./input/{filename}"):
            ret['filename'] = filename.replace('jpg', 'png')
            if os.path.exists(f"./output/{ret['filename']}"):
                ret['status'] = 1
                ret['tip'] = '转换完成！'
            else:
                ret['status'] = 0
                ret['tip'] = '转换中...'
        return jsonify(ret)



# 文件下载 /download
@app.route('/download/<type>/<filename>', methods=['GET'])
def download(type, filename):
    if request.method == "GET":
        if type == 'input' or type == 'output':
            if os.path.exists(f"{type}/{filename}"):
                return send_from_directory(type, filename, as_attachment=True)
            else: return 'file not exist'
        else:  return 'type error'
        
    
    
if __name__ == '__main__':
   # CORS(app, supports_credentials=True) #跨域
   app.run(debug=True, host='0.0.0.0', port=9000)