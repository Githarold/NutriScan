#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os

# 서버의 업로드 URL 설정
upload_url = 'http://localhost:5000/upload'

# 업로드할 파일의 경로 설정
file_path = '/home/seongbin/workspace/img/je6.png'  # 여기에 업로드할 이미지 파일의 경로를 입력하세요.
additional_text = 'Your text here'  # 서버에 보낼 추가 문자열

# 파일이 존재하는지 확인
if not os.path.isfile(file_path):
    print("File not found!")
    exit()

# 파일을 멀티파트 형식으로 업로드
with open(file_path, 'rb') as f:
    files = {'file': (os.path.basename(file_path), f)}
    data = {'text': additional_text}
    response = requests.post(upload_url, files=files, data=data)

# 서버의 응답 출력
print(response.text)
