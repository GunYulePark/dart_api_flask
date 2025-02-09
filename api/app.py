from flask import Flask, request, jsonify, send_file
import os
import dart_fss as dart
from dotenv import load_dotenv


app = Flask(__name__)

# 환경 변수 로드
load_dotenv()
api_key = os.getenv('DART_API_KEY')

if not api_key:
    raise ValueError("DART API KEY is missing. Set it in the .env file.")

dart.set_api_key(api_key=api_key)

# DART에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

@app.route('/')
def index():
    return "Welcome to the Flask DART API integration! Use /download to fetch financial statements."

@app.route('/download', methods=['GET'])
def download():
    try:
        # URL 파라미터 받기
        corp_name = request.args.get('corp_name', '종근당')
        bgn_de = request.args.get('bgn_de', '20240101')
        report_tp = request.args.get('report_tp', 'annual')

        # 회사 찾기
        corp = corp_list.find_by_corp_name(corp_name, exactly=True)
        if not corp:
            return jsonify({"error": "Company not found."}), 404

        corp_audit = corp[0]

        # 재무제표 추출
        corp_fs = corp_audit.extract_fs(bgn_de=bgn_de, separate=True, report_tp=[report_tp])

        # 엑셀 파일 저장
        file_path = os.path.join(os.getcwd(), 'corp_fs.xlsx')
        corp_fs.save(file_path)

        # 파일 반환
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
