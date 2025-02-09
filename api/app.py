from flask import Flask, request, jsonify, send_file
import os
import dart_fss as dart


app = Flask(__name__)

# 환경 변수 로드
api_key = os.getenv('DART_API_KEY')

if not api_key:
    raise ValueError("DART API KEY is missing. Set it in the .env file.")

dart.set_api_key(api_key=api_key)

# DART에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()




if __name__ == '__main__':
    app.run(debug=True)
