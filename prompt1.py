from flask import Flask, request
from bardapi import BardCookies
from langchain import PromptTemplate
import json
import os

# Json형태의 데이터 예시 1번
# 문제, 조건들, 학생이 제출한 코드가 Json형태로 변수명 json_data에 담겨져 있다
json_data = {
    "문제" :"1부터 30까지의 숫자 중 3의 배수를 출력하시오.",
    "조건1" : "1 <= num <= 30",
    "조건2" : "변수명으로 num을 사용하시오.",
    "조건3" : "for문과 range함수를 사용하시오.",
    "코드": """for num in range(3, 31, 3):
                    print(num)"""
}

# ===================================== #

# Flask객체를 app변수에 담기
app = Flask(__name__)


# Flask 가상 서버 열기
@app.route('/')  # URL 설정
def test1():

    # json_data의 항목별로 각각 변수에 담기
    code = json_data["코드"]
    condition_1 = json_data["조건1"]
    condition_2 = json_data["조건2"]
    condition_3 = json_data["조건3"]
    
    # Json형태의 데이터를 제대로 받았고, 항목별로 각각의 변수에 알맞게 담았는지 콘솔창에 출력해서 확인하기
    print("학생이 제출한 코드 : " + code, "/", "조건1번 : " + condition_1,  "/", "조건2번 : " + condition_2,  "/", "조건3번 : " + condition_3)

    # Bard API에 연결하기 (쿠기값 = 인증정보)
    def getbard():
        cookie_dict = {
            "__Secure-1PSID": "cAgpBR5S2ndRr9iunxvCyyo7YFXqq36iX-Rodu3BIPIDGzCa9Qaebv-8r1cunrslg9rkkQ.",            # 매번 바뀌므로 주의
            "__Secure-1PSIDTS": "sidts-CjEB3e41hTiawxdoYxE_H_rf-RsCCvyY98-8lGRSl9io59F1ttmvGE8eKnYD8EmilRKcEAA", }  # 매번 바뀌므로 주의

        # Bard_API와 상호작용할 수 있는 객체 만들기 및 인증정보 전달하기
        bard = BardCookies(cookie_dict=cookie_dict)

        # 넘겨 받은 데이터의 채점을 Bard에게 부탁하기 (LangChain의 PromptTemplate 사용 : 변수를 여러개 지정할 수 있다)
        # code : 학생이 제출한 코드를 담을 변수
        # result : 학생이 제출한 코드를 실행했을 때 나오는 결과값을 담을 변수
        # condition1,2,3 : 조건1,2,3의 조건 부합 여부 결과(통과 / 실패)를 담을 변수
        multiple_input_prompt = PromptTemplate(input_variables=['code', 'result', 'condition1', 'condition2', 'condition3'],
                                               template="""
                                                       '{code}'
                         당신은 정답과 조건을 확인하여 이미 짜여진 양식에 맞춰 답을 해주는 단답형 채점기입니다.                             
                         이것에 대한 답변은 반드시 아래와 같은 양식으로만 출력해주세요.
                         -정답 : '{result}',
                         -조건1 : '{condition1}',
                         -조건2 : '{condition2}',
                         -조건3 : '{condition3}'
                         이 양식에 해당되는 답변 이외의 설명, 부가설명, 해설, 결과는 필요하지 않으므로 출력하지 않습니다.
                         """)


        # Bard의 답변을 콘솔창에 출력해보기
        print(bard.get_answer(
            multiple_input_prompt.format(code=code, result="code의 실행 결과값 전부 출력", condition1=f"{condition_1}조건에 부합하면 <통과> 출력, 부합하지 않으면 <실패> 출력",
                                         condition2=f"{condition_2}조건에 부합하면 <통과> 출력, 부합하지 않으면 <실패> 출력",
                                         condition3=f"{condition_3}조건에 부합하면 <통과-end> 출력, 부합하지 않으면 <실패-end> 출력"))['content'])

        # Bard의 답변을 judgement변수에 담기
        judgement = bard.get_answer(
            multiple_input_prompt.format(code=code, result="code의 실행 결과값 전부 출력", condition1=f"{condition_1}조건에 부합하면 <통과> 출력, 부합하지 않으면 <실패> 출력",
                                         condition2=f"{condition_2}조건에 부합하면 <통과> 출력, 부합하지 않으면 <실패> 출력",
                                         condition3=f"{condition_3}조건에 부합하면 <통과-end> 출력, 부합하지 않으면 <실패-end> 출력"))['content']
        
        
        
        # Bard의 답변을 return하기
        return judgement

    # Bard 스크립트의 main함수 정의하기
    def main():
        # getbard()함수가 실행된 결과를 judgement 변수에 담아서 return 해주기
        judgement = getbard()
        return judgement

    # Bard 스크립트 main함수 실행 및 judgement변수에 담기
    judgement = main()

    # Bard의 답변에서 정답과 조건들만 뽑아내기(파싱)
    # "**" : 파싱 시작 위치
    a_index = judgement.find("**")
    
    # "end" : 파싱 끝 위치
    b_index = judgement.find("end")

    # 파싱 끝낸 결과값 final변수에 담기
    final = judgement[a_index:b_index + 4]
    print("☆파싱 시작-> ", final, " <- 파싱 끝☆")

    # Bard 스크립트가 직접 실행될 때만 main()함수 호출하도록 하는 파이썬의 관례적인 코드
    if __name__ == "__main__":
        main()

    # 파싱 끝낸 결과값인 final변수 return하기 (가상서버에 출력)
    return final


# Flask객체의 뷰함수 실행
if __name__ == '__main__':
    app.run()