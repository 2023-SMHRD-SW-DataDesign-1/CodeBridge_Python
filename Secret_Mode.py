from flask import Flask, request
from bardapi import Bard
from flask_cors import CORS
import json

# ========================================================================= # Flask의 함수 시작
# Flask객체를 app변수에 담기
app = Flask(__name__)
app(CORS)


# Flask 가상 서버 열기
@app.route('/', methods=['GET', 'POST'])  # URL 설정
def test2():

    print("리퀘스트 확인 :", request)
    if request.method == 'GET':
        return "GET Connect"
    elif request.method == 'POST':
        print("json_date 받음 :", request.get_json())
        json_data = request.get_json()

    # 받은 데이터의 value값 항목별로 변수에 담기
    test_condition = []
    for key, value in json_data.items():
        for w in key:
            if w[0] == 'p':
                problem_content = value
            elif w[0] == 't':
                test_condition.append(value)
            elif w[0] == 's':
                sub_code = value



    # Bard에 연결하기
    # 토큰 준비하기 (크롬의 시크릿창으로 Bard홈페이지에 접속하여 cookie값 가져오기)
    token = 'cAgpBdH-6aA5yETpDrnD3uOERXqRMAreAc_mjWvzmNs8IYDcP-lkg31aOvOxDm_wTDXR1Q.'

    # Bard의 답변을 bard_answer변수에 담기
    bard_answer = Bard(token=token).get_answer(
                 f''' 
                    문제 :
                    {problem_content}
                    제출한 코드 :
                    {sub_code}
                    제한조건 :
                    {test_condition}
                    
                    아래의 1번, 2번의 문장으로만 대답해야해. 그 이외의 답변이나 설명은 절대 하지마.
                    1번. 작성된 코드를 판단해서 => [[정답 or 오답]] 반드시 이 형식으로 출력해줘.
                    2번. 작성된 코드의 조건을 판단해서  => <<조건n번 : 만족 or 불만족, 조건n번: 만족 or 불만족, ...>> 반드시 이 형식으로 출력해줘.
                    '''
                 )['content']

    # Bard의 답변 출력하기
    print("Bard채점결과 :", bard_answer)

    # Bard의 답변을 파싱하기
    # 코드실행결과 -> 정답 or 오답
    start1_index = bard_answer.find("<<")
    end1_index = bard_answer.find(">>")

    # 조건부합결과 -> 만족 or 불만족
    start2_index = bard_answer.find("[[")
    end2_index = bard_answer.find("]]")

    # 파싱된 최종결과값 parse_result변수에 담기
    parse_result = []
    parse_result.append(bard_answer[start1_index: end1_index + 2])
    parse_result.append(bard_answer[start2_index: end2_index + 2])

    # 파싱된 결과 출력하기
    print("파싱된 최종 답변 :", parse_result)

    # 채점 결과값 Spring으로 보내기
    # url = "http://localhost:8080/..." # 스프링 엔드포인트(HTTP요청을 처리하는 경로)
    # response = requests.post(url, data=final)
    # print(response.text)

    # 파싱 끝낸 결과값인 final변수 return하기 (Flask함수 실행되면 return해서 가상서버에 출력)

    return parse_result


# Flask 실행
if __name__ == '__main__':
    app.run()
