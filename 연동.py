from flask import Flask, request, render_template
from flask_cors import CORS
import json

# Flask객체를 app변수에 담기
app = Flask(__name__)
CORS(app)


# Flask 가상 서버 열기
@app.route("/", methods=['GET', 'POST'])  # URL 설정
def test1():
    print('리퀘스트 확인', request)

    if(request.method == 'GET'):
        return "GET ok"
    elif(request.method == 'POST'):
        print('리퀘스트 확인1', request.get_json())
        return "POST ok"

    print(request.form['sub_code'])

    # 요청의 Content-Type 헤더를 "application/json"으로 설정합니다.
    # judgement = request.get_json()
    # print(judgement)


# Flask 실행
if __name__ == '__main__':
    app.run()
