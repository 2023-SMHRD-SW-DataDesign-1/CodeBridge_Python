import os
import replicate
from flask import Flask, request


# Json형태의 데이터 예시 4번
json_data = { "문제": "입력받은 두 정수의 최대공약수를 구하시오.",
            "난이도": "중",
            "조건1": "입력받은 두 정수는 1 이상 100 이하의 정수이다.",
            "조건2": "유클리드 호제법을 사용하시오.",
            "코드": """ def gcd(x, y): while y != 0: x, y = y, x % y return x x = int(input()) y = int(input()) print(gcd(x, y)) """,
            "문제생성": "생성완료3" }

# ========================================================================= # Flask의 함수 시작
# Flask객체를 app변수에 담기
app = Flask(__name__)


# Flask 가상 서버 열기
@app.route('/')  # URL 설정
def test1():


    # ========================================================================= # 받은 데이터의 key와 value 각각 변수에 담기

    # json_data의 key의 첫글자에 따라 변수명을 달리하여 key와 value의 값을 담기
    condition = []
    condition_value = []
    for key, value in json_data.items():
        for w in key:
            if w[0] == '문':
                problem = key
                problem_value = value
            elif w[0] == '조':
                condition.append((key))
                condition_value.append(value)
            elif w[0] == '코':
                code = key
                code_value = value

    # ========================================================================= # Llama2_api 시작
    # api_toekn 설정

    os.environ["REPLICATE_API_TOKEN"] = api_token

    #
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={"prompt":   f''' 
                       ->Grading,
                        {problem} : {problem_value}
                        {code} : {code_value}
                       Answer only with the word 'correct' if the code is viable and 'wrong answer' if it is not viable. 
                       Please don't explain anything else.
                       And there are conditions when answering.
                       The answer must be printed in the form of a dictionary, such as <"execution result": "correct" or "wrong answer.">
                       And please print '->Grading' at the top, and print '<-Grading' at the bottom.
                       Please don't give any explanation except for those 2 answers based on (:)colon.
                       
                       =>Check,
                        {condition} : {condition_value}
                        {code} : {code_value}
                        Answer only with the word 'pass' if the code perfectly meets each condition, or 'fail' if it doesn't perfectly meet. Please don't explain anything else.
                        And there are conditions when answering.
                        The answer must be printed in the form of a list by dividing each condition match result into a comma(,) in the list, such as ['condition1' : 'pass' or 'fail', 'condition2' : 'pass' or 'fail'].
                        .Please don't explain anything except those 2 answers based on the colon.
                        And please print '=>Check' at the top and print '<=Check' at the bottom.
                     ''', "temperature" : 0.75})

    for item in output:
        judgement = item
        print(judgement, end="")

    # Llama2의 답변에서 정답과 조건들만 뽑아내기(파싱)
    # 파싱 시작 위치 설정
    # a_index = judgement.find("<Grading>") + len("<Grading>")
    a_index = judgement.find("->")
    # c_index = judgement.find("Second")

    # 파싱 끝 위치 설정
    # b_index = judgement.find("</Grading>")
    b_index = judgement.find("<-")
    # d_index = judgement.find("]")

    # 파싱 끝낸 결과값 final변수에 담고 콘솔창에 출력해보기
    final = judgement[a_index : b_index]
    # final = judgement[a_index:b_index].strip()
    # final += judgement[c_index : d_index + 4]
    print("☆파싱 시작-> ", final, " <- 파싱 끝☆")

    # ========================================================================= #



    # 파싱 끝낸 결과값인 final변수 return하기 (Flask함수 실행되면 return해서 가상서버에 출력)
    return final

# ========================================================================= # Flask 함수 실행

# Flask 실행
if __name__ == '__main__':
    app.run()


