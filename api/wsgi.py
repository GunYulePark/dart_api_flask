import sys
import os

# 현재 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(__file__))

from app import app  # app.py가 api/ 폴더 안에 있어야 함

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


if __name__ == "__main__":
    app.run()