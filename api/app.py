import os
from flask import Flask, request, jsonify, send_file
import dart_fss as dart

app = Flask(__name__)

# 환경 변수에서 API 키 불러오기
api_key = os.getenv('DART_API_KEY')

if not api_key:
    raise ValueError("DART API KEY is missing. Set it in Render Environment Variables.")

dart.set_api_key(api_key=api_key)

@app.route('/')
def index():
    return "Welcome to the Flask DART API integration! Use /download to fetch financial statements."

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render에서 환경 변수로 포트 할당
    app.run(host="0.0.0.0", port=port, debug=True)



