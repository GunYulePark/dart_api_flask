from flask import Flask, request, jsonify, send_file
import os
import dart_fss as dart

app = Flask(__name__)

# 환경 변수에서 API 키 불러오기
api_key = os.getenv('DART_API_KEY')

if not api_key:
    raise ValueError("DART API KEY is missing. Set it in Render Environment Variables.")

dart.set_api_key(api_key=api_key)

def get_corp_list():
    """기업 리스트를 가져오되, 'corp_eng_name' 필드는 제거"""
    corp_data = dart.get_corp_list()
    
    # corp_eng_name 필터링 (오류 방지)
    cleaned_corp_data = []
    for corp in corp_data:
        corp_dict = corp.to_dict()
        corp_dict.pop("corp_eng_name", None)  # 'corp_eng_name' 키 제거
        cleaned_corp_data.append(corp_dict)

    return cleaned_corp_data

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

        # ✅ `get_corp_list()` 실행하여 기업 목록 가져오기 (필터링 적용)
        corp_list = get_corp_list()
        corp = next((c for c in corp_list if c["corp_name"] == corp_name), None)

        if not corp:
            print("Company not found.")  # 로그 추가
            return jsonify({"error": "Company not found."}), 404

        # Corp 객체 다시 생성 (필터링된 데이터 사용)
        corp_audit = dart.Corp(**corp)

        # 재무제표 추출
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
