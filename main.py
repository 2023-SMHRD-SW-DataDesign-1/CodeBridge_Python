from flask import Flask, render_template, request
from bardapi import BardCookies
from langchain import PromptTemplate
import json
import os



### 1. Flask의 tes1()함수 안에서 Bard 실행시키는 방법

# Json 데이터 예시
json_data = {
    "Code" : "2+(3*4)",
}


# Flask 객체를 app변수에 담기
app = Flask(__name__)

# Flask 가상 서버 열기
@app.route('/')
def test1():

    # (3) json데이터 예시 받기
    print("Json데이터 예시 : ", json_data)

    result = json_data["Code"]


    # Bard API에 연결하기
    def getbard():
        cookie_dict = {
            "__Secure-1PSID": "",
            "__Secure-1PSIDTS": "", }  # 매번 바뀌므로 주의

        # Bard API와 상호작용할 수 있는 인스턴스 만듦. 인증정보 전달
        bard = BardCookies(cookie_dict=cookie_dict)


        # Bard에게 채점 부탁하기
        # print(bard.get_answer("""
        #        {0}
        #        이거에 대한 답변을 반드시 아래와 같은 json형식의 틀에 맞춰서 답변해주세요.
        #         ["Code" : "Code의 계산 결과 출력",
        #         "Condition1" : "Code가에 사칙연산 포함하면 '포함', 포함하지 않으면 '포함안함' 출력",
        #         "Condition2" : "Code가 for문 포함하면 '포함', 포함하지 않으면 '포함안함' 출력"]
        #         꼭 이 형식으로만 답변해주세요.
        #                    """.format(result))['content'])
        #
        # # Bard답변 변수에 담기
        # from_bard = bard.get_answer("""
        #        {0}
        #        이거에 대한 답변을 반드시 아래와 같은 json형식의 틀에 맞춰서 답변해주세요.
        #         ["Code" : "Code의 계산 결과 출력",
        #         "Condition1" : "Code가에 사칙연산 포함하면 '포함', 포함하지 않으면 '포함안함' 출력",
        #         "Condition2" : "Code가 for문 포함하면 '포함', 포함하지 않으면 '포함안함' 출력"]
        #         꼭 이 형식으로만 답변해주세요.
        #                    """.format(result))['content']
        # return from_bard

        # 2개의 변수 지정할 때
        multiple_input_prompt = PromptTemplate(input_variables=['result','condition1', 'condition2'],
                                               template="""
                                               '{result}'
                이거에 대한 답변을 반드시 아래와 같은 json형식의 틀에 맞춰서 답변해주세요.
                 "Code" : "Code의 계산 결과 출력",
                 "Condition1" : "'{condition1}'",
                 "Condition2" : "'{condition2}'",
                 꼭 이 형식으로만 답변해주세요.""")

        # print(multiple_input_prompt.format(condition1='for문이 포함되어 있어야 한다', condition2='변수명 add가 포함되어 있어야 한다'))

        print(bard.get_answer(
             multiple_input_prompt.format(result = result, condition1="Code가에 사칙연산 포함하면 '포함', 포함하지 않으면 '포함안함' 출력", condition2="Code가 for문 포함하면 '포함', 포함하지 않으면 '포함안함' 출력"))['content'])

        from_bard = bard.get_answer( multiple_input_prompt.format(result = result, condition1="Code가에 사칙연산 포함하면 '포함', 포함하지 않으면 '포함안함' 출력", condition2="Code가 for문 포함하면 '포함', 포함하지 않으면 '포함안함' 출력"))['content']

        return from_bard

    # Bard 스크립트의 메인 함수
    def main():
        from_bard = getbard()
        return from_bard

    from_bard = main()

    # Bard 스크립트가 직접 실행될 때만 main()함수 호출하도록 하는 파이썬의 관례적인 코드
    if __name__ == "__main__":
        main()

    return result + "성공!" + from_bard

# Flask객체의 뷰함수 실행
if __name__ == '__main__':
    app.run()