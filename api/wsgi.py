import sys
import os

# 현재 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(__file__))

from app import app  # app.py가 api/ 폴더 안에 있어야 함

if __name__ == "__main__":
    app.run()