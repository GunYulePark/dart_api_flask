from flask import Flask, request, jsonify, send_file
import os
import dart_fss as dart


app = Flask(__name__)

# 환경 변수 로드
api_key = os.getenv('DART_API_KEY')

if not api_key:
    raise ValueError("DART API KEY is missing. Set it in the .env file.")

dart.set_api_key(api_key=api_key)



@app.route('/')
def index():
    return "Welcome to the Flask DART API integration! Use /download to fetch financial statements."

@app.route('/download', methods=['GET'])
def download():
    try:
        corp_name = request.args.get('corp_name', '종근당')
        bgn_de = request.args.get('bgn_de', '20240101')
        report_tp = request.args.get('report_tp', 'annual')

        # 회사 리스트 가져오기 (서버 시작 시 실행하지 않고 필요할 때만 실행)
        corp_list = get_corp_list()
        corp = corp_list.find_by_corp_name(corp_name, exactly=True)

        if not corp:
            return jsonify({"error": "Company not found."}), 404

        corp_audit = corp[0]

        # 재무제표 추출
        corp_fs = corp_audit.extract_fs(bgn_de=bgn_de, separate=True, report_tp=[report_tp])

        # 임시 파일 저장
        file_path = "corp_fs.xlsx"
        corp_fs.save(file_path)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render에서 환경 변수로 포트 할당
    print(f"Starting Flask server on port {port}...")  # 포트 확인용 로그 추가
    app.run(host="0.0.0.0", port=port, debug=True)



