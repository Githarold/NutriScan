#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import webbrowser

# webbrowser.open("http://localhost:5000")
session = requests.Session()
# 서버의 업로드 URL 설정
page = requests.get("http://110.34.114.31:5000/check")
print(page.text)