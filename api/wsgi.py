import sys
import os

# 현재 디렉토리를 sys.path에 추가하여 Render가 app.py를 찾을 수 있도록 설정
sys.path.insert(0, os.path.dirname(__file__))

from app import app  # app.py가 api/ 폴더 안에 있어야 함

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render에서 환경 변수로 포트 할당
    app.run(host="0.0.0.0", port=port)