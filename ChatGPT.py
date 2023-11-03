import os
import openai
from flask import Flask, request
from flask_cors import CORS
import json


# Flask객체를 app변수에 담기
app = Flask(__name__)
CORS(app)


# Flask함수 정의하기
@app.route("/", methods=['GET', 'POST'])  # URL 설정
def test1():
    
    # 받은 데이터 각각 변수에 담기
    if(request.method == 'GET'):
        return "GET ok"
    elif(request.method == 'POST'):
        request_data = request.get_json()
        problem_content = request_data.get("test_contents")
        sub_code = request_data.get("sub_code")
        test_condition = request_data.get("test_condition")


    # ChatGPT 연결하기
    # OPENAI API 키 입력하기
    openai.api_key = ""

    # ChatGPT에게 역할 부여 및 호출하기
    messages = [ {"role" : "system", "content" : "gpt야, 너는 단답형 채점기야"}]


    content = f'''
                문제 :
                # {problem_content}
                # 제출한 코드 :
                # {sub_code}
                # 제한조건 :
                # {test_condition}
                # 
               아래의 1번, 2번의 형식화된 문장으로만 대답해야해. 그 이외의 답변이나 설명은 절대 하지마.
                1번. 작성된 코드를 판단해서 => [[정답 or 오답]] 반드시 이 형식으로 출력해줘.
                2번. 작성된 코드의 조건을 판단해서  => <<조건n번 : 만족 or 불만족, 조건n번: 만족 or 불만족, ...>> 반드시 이 형식으로 출력해줘.
                '''

    messages.append({"role" : "user", "content" : content})

    completion = openai.ChatCompletion.create(
                                                model="gpt-3.5-turbo",
                                                messages=messages,
                                                temperature=0
                                                )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT : {chat_response}')

    # ChatGPT의 답변을 파싱하기
    # 코드실행결과 -> 정답 or 오답
    start1_index = chat_response.find("<<")
    end1_index = chat_response.find(">>")

    # 조건 부합결과 -> 만족 or 불만족
    start2_index = chat_response.find("[[")
    end2_index = chat_response.find("]]")

    parse_result = []
    parse_result.append(chat_response[start1_index: end1_index + 2])
    parse_result.append(chat_response[start2_index: end2_index + 2])

    # 파싱된 결과 출력하기
    print("&&파싱된 최종 답변&& :", parse_result)

    # 채점 결과값 Spring으로 보내기
    # url = "http://localhost:8080/..." # 스프링 엔드포인트(HTTP요청을 처리하는 경로)
    # response = requests.post(url, data=final)
    # print(response.text)

    # 파싱 끝낸 결과값인 final변수 return하기 (Flask함수 실행되면 return해서 가상서버에 출력)

    return parse_result


# Flask 실행
if __name__ == '__main__':
    app.run()
