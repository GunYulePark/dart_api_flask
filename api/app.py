from flask import Flask, request, jsonify, send_file
import os
import dart_fss as dart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 활성화

# 환경 변수에서 API 키 불러오기
api_key = os.getenv('DART_API_KEY')

if not api_key:
    raise ValueError("DART API KEY is missing. Set it in Render Environment Variables.")

dart.set_api_key(api_key=api_key)

# ✅ `get_corp_list()` 함수 정의 추가 (Flask 실행 전 정의해야 함)
def get_corp_list():
    """필요할 때만 dart_fss에서 기업 목록을 불러옴"""
    return dart.get_corp_list()

@app.route('/')
def index():
    return "Welcome to the Flask DART API integration! Use /download to fetch financial statements."

@app.route('/download', methods=['GET'])
def download():
    try:
        corp_name = request.args.get('corp_name', '종근당')
        bgn_de = request.args.get('bgn_de', '20240101')
        report_tp = request.args.get('report_tp', 'annual')

        print(f"Received request: corp_name={corp_name}, bgn_de={bgn_de}, report_tp={report_tp}")  # 로그 추가

        # ✅ `get_corp_list()` 실행하여 기업 목록 가져오기
        corp_list = get_corp_list()
        corp = corp_list.find_by_corp_name(corp_name, exactly=True)

        if not corp:
            print("Company not found.")  # 로그 추가
            return jsonify({"error": "Company not found."}), 404

        corp_audit = corp[0]
        corp_fs = corp_audit.extract_fs(bgn_de=bgn_de, separate=True, report_tp=[report_tp])

        # 파일 저장
        file_path = "corp_fs.xlsx"
        corp_fs.save(file_path)
        print(f"File saved: {file_path}")  # 로그 추가

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {str(e)}")  # 오류 로그 추가
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render에서 환경 변수로 포트 할당
    print(f"Starting Flask server on port {port}...")  # 포트 확인용 로그 추가
    app.run(host="0.0.0.0", port=port, debug=True)
