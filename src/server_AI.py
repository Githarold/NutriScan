#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

app = Flask(__name__)
train_best = os.path.normpath(os.path.join(current_path, './best.pt'))
model=YOLO(train_best)



# 이미지를 저장할 경로 설정
UPLOAD_FOLDER = '/home/seongbin/workspace/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    additional_text = request.form.get('text', '')  # 클라이언트로부터 받은 문자열
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 파일 저장 경로
        file.save(file_path)
        
        # YOLO 모델을 사용하여 이미지 분석
        results = model.predict(source=file_path, save=True)

        print(f'Uploaded file: {filename}')
        return f'File uploaded successfully: {filename}, Text: {additional_text}'
    else:
        return 'Invalid file type'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
