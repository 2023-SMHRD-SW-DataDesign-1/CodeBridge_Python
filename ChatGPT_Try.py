# 필요한 라이브러리 불러오기
import openai
from flask import Flask, request
from flask_cors import CORS
import os
import json

# Flask객체를 app변수에 담기
app = Flask(__name__)
CORS(app)


# Flask함수 정의하기
@app.route("/", methods=['GET', 'POST'])  # URL 설정
def test1():
    # 받은 데이터 각각 변수에 담기
    if (request.method == 'GET'):
        return "GET ok"
    elif (request.method == 'POST'):
        request_data = request.get_json()

        # problem_content : 문제
        problem_content = request_data.get("test_contents")
        # sub_code : 학생이 제출한 코드
        sub_code = request_data.get("sub_code")
        # test_conditions = 문제의 조건
        test_conditions = request_data.get("test_condition")

    # ChatGPT 연결하기
    # OPENAI API 키 입력하기
    openai.api_key = "xxxx"

    # ChatGPT에게 역할 부여 및 호출하기
    messages = [{"role": "system", "content": "You're a scorer who distinguishes between the correct and incorrect answers in the code."}]

    # prompt 작성하기
    content = f'''
        - 문제 : {problem_content},
        - 문제의 조건 : {test_conditions},
        - 학생이 제출한 코드 : {sub_code}
        
        위에 문제와 문제의 조건, 학생이 제출한 코드가 있습니다.
        학생이 제출한 코드를 임의로 수정하지 마십시오.
        채점해야할 항목은 2가지 입니다.
        첫번째, 학생이 제출한 코드가 문제의 요구사항을 완벽히 충족하여 올바른 출력값을 생성하는 경우 "<올바른 코드입니다.>"의 문장을 출력하세요.
               잘못된 출력값을 생성하는 경우 "<잘못된 코드입니다.>"의 문장을 출력하세요.
        
        두번째, 학생이 제출한 코드를 문제의 조건에 따라 각각 만족하는지 판단해서 만족하는 경우 "[[만족합니다]]"의 문장을 만족하는 조건의 갯수만큼 출력하세요.
               만족하지 않는 경우 "[[만족하지 않습니다.]]"의 문장을 만족하지 않는 조건의 갯수만큼 출력하세요.
       
        첫번째 결과와 두번째 결과의 문장들을 "&&"이 기호를 사용하여 이어붙여서 출력하세요.
        '''

    messages.append({"role": "user", "content": content})


    completion = openai.ChatCompletion.create(
                                                model="gpt-3.5-turbo",
                                                messages=messages,
                                                temperature=0.5,
                                             )


    chat_response = completion.choices[0].message.content
    print(f'ChatGPT의 답변 : {chat_response}')


    ## 문제의 정답여부와 조건만족여부 ##
   #  1번 -문제 : 올바른 코드입니다
   #      -조건 : 만족합니다
   #
   #  2번 -문제 : 잘못된 코드입니다
   #      -조건 : 만족합니다
   #
   #  3번 -문제 : 잘못된 코드입니다
   #      -조건 : 만족하지 않습니다
   #
   #  4번 -문제 : 올바른 코드입니다
   #      -조건 : 만족합니다, 만족하지 않습니다
   #
   # 5번 -문제 : 올바른 코드입니다
   #     -조건 : 만족합니다


    # ChatGPT의 답변을 파싱하기
    # 코드실행결과 -> 정답 or 오답
    # start1_index = chat_response.find("[")
    # end1_index = chat_response.find("]")
    #
    # # 조건 부합결과 -> 만족 or 불만족
    # start2_index = chat_response.find("<<")
    # end2_index = chat_response.find(">>")
    #
    # parse_result = []
    # parse_result.append(chat_response[start1_index: end1_index + 2])
    # parse_result.append(chat_response[start2_index: end2_index + 2])

    # 파싱된 결과 출력하기
    # print("&&파싱된 최종 답변&& :", parse_result)

    # 채점 결과값 Spring으로 보내기
    # url = "http://localhost:8080/..." # 스프링 엔드포인트(HTTP요청을 처리하는 경로)
    # response = requests.post(url, data=final)
    # print(response.text)



    # 파싱 끝낸 결과값인 final변수 return하기 (Flask함수 실행되면 return해서 가상서버에 출력)
    return "ok"


# Flask 실행
if __name__ == '__main__':
    app.run()
