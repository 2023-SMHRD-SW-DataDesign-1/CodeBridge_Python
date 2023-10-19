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
    if (request.method == 'GET'):
        return "GET ok"
    elif (request.method == 'POST'):
        request_data = request.get_json()
        problem_content = request_data.get("test_contents")
        sub_code = request_data.get("sub_code")
        test_condition = request_data.get("test_condition")



    # OpenAI객체 생성
    completion = openai.Completion

    # 연결 설정
    # OpenAI config
    temperature = 0.0
    # 생성되는 텍스트의 창의성 제어 (값이 높을수록 창의적)
    top_p = 0.0
    # 생성되는 텍스트의 다양성 제어 (값이 높을수록 다양)
    best_of = 1
    # 생성되는 텍스트의 횟수 제어 (1인경우 한번만, 10이면 열번 생성)
    frequency_penalty = 0.0
    # 생성되는 텍스트의 빈도 제어 (값이 높을수록 더 드문 단어 사용)
    presence_pentaly = 0.0
    # 생성되는 텍스트의 존재감 제어 (값이 높을수록 더 많은 단어 사용)

    # load API key
    openai.api_key = ""

    # prompt 작성
    prompt =  f'''
                문제 :
                # {problem_content}
                # 제출한 코드 :
                # {sub_code}
                # 제한조건 :
                # {test_condition}
                # 
               아래의 1번, 2번의 형식화된 문장으로만 대답해야해. 그 이외의 답변이나 설명은 절대 하지마.
               그리고 1번과 2번 답변 사이에 한 단락을 띄워줘.
                1번. 작성된 코드를 판단해서 => "1번. 정답 or 오답 입니다" 반드시 이 형식으로 출력해줘.
                2번. 작성된 코드의 조건을 판단해서  => 2번. "조건n번 : 만족 or 불만족, 조건n번: 만족 or 불만족,..." 반드시 이 형식으로 출력해줘.
                '''

    # API 호출
    def ask_for_short_answer(prompt):
        response = completion.create(
            prompt=prompt,
            # 생성할 초기 텍스트
            model="text-davinci-003",
            # 사용할 모델
            max_tokens=500,
            # 생성할 텍스트의 최대 토큰 수 (1토큰=1개의 단어 또는 구)
            temperature=temperature,
            top_p=top_p,
            best_of=best_of,
        )

        return response.choices[0].text.strip()

    result = ask_for_short_answer(prompt)
    print(result)

    # ChatGPT의 답변을 파싱하기
    # 코드실행결과 -> 정답 or 오답
    start1_index = result.find("1번")
    end1_index = result.find("입니다")

    # 조건 부합결과 -> 만족 or 불만족
    start2_index = result.find("2번")

    parse_result = []
    parse_result.append(result[start1_index : end1_index + 4])
    parse_result.append(result[start2_index : ])

    # 파싱된 결과 출력하기
    print("&&파싱된 최종 답변&& :", parse_result)
    
    return parse_result

# Flask 실행
if __name__ == '__main__':
    app.run()
