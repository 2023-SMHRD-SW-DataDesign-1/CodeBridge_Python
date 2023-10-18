from flask import Flask, request
from bardapi import BardCookies
from langchain import PromptTemplate
import json
import os

### 스프링에서 받은 Json데이터에서 조건의 갯수가 정해져있지 않은 경우 => 원하는 결과만 파싱해서 return가능!
# LangChain의 PromptTemplate 사용X

# Json형태의 데이터 예시 1번
# 문제, 조건들, 학생이 제출한 코드가 Json형태로 변수명 json_data에 담겨져 있다
json_data = {
    "문제": "1부터 30까지의 숫자 중 3의 배수를 출력하시오.",
    "조건1": "1 <= num <= 30",
    "조건2": "변수명으로 codenum을 사용하시오.",
    "조건3": "for문과 range함수를 사용하시오.",
    "실행결과" : "null",
    "코드": """for num in range(3, 31, 3):
                    print(num),                
                    """
}

# ===================================== #

# Flask객체를 app변수에 담기
app = Flask(__name__)


# Flask 가상 서버 열기
@app.route('/')  # URL 설정
def test1():
    # (1) json_data 예시1번의 해당 항목별로 각각 변수에 담기
    # for key, value in json_data.items():
    #     globals()[key] = value


    # print("문제", 문제)
    # print("코드", 코드)
    # print("조건1", 조건1)
    # print("조건2", 조건2)
    # print("조건3", 조건3)
    # print("실행결과", 실행결과)



    # (2) josn_data를 Json파일로 받을 경우
    # with open('json_data.json') as f:
      # json_obj =json.load(f)

    # code = json_obj["코드"]
    # condition_1 = json_obj["조건1"]
    # condition_2 = json_obj["조건2"]
    # condition_3 = json_obj["조건3"]


    # (3) json_data를 GET 또는 POST방식으로 받을 경우
    # @app.rounte('/', methods=['POST'])
    # def test1():
        # params = request.get_json()

        # json_data의 key값을 변수에 담기
        # for key, value in params.items():
            # globals()[key] = value
        # 변수의 값 출력
        # print("코드 : " + 코드)
        # print("조건1 : " + 조건1)
        # print("조건2 : " + 조건2)
        # print("조건3 : " + 조건3)


    # Bard API에 연결하기 (쿠기값 = 인증정보)
    def getbard():
        cookie_dict = {
            "__Secure-1PSID": "cAgpBR5S2ndRr9iunxvCyyo7YFXqq36iX-Rodu3BIPIDGzCa9Qaebv-8r1cunrslg9rkkQ.",  # 매번 바뀌므로 주의
            "__Secure-1PSIDTS": "sidts-CjEB3e41hV6Ow5vxerY5C8D09zp_qSOcT8AajXZvt0H8y4YiO1nQ1aQJVxAwqpQjg-ssEAA", }  # 매번 바뀌므로 주의

        # Bard_API와 상호작용할 수 있는 객체 만들기 및 인증정보 전달하기
        bard = BardCookies(cookie_dict=cookie_dict)


        # code : 학생이 제출한 코드를 담을 변수
        # result : 학생이 제출한 코드를 실행했을 때 나오는 결과값을 담을 변수
        # condition1,2,3 : 조건1,2,3의 조건 부합 여부 결과(통과 / 실패)를 담을 변수

        con = []
        con_value = []
        for key, value in json_data.items():
            for w in key:
                if w[0] == '문':
                    problem = key
                    problem_value = value
                elif w[0] == '조':
                    con.append((key))
                    con_value.append(value + " 해당 조건에 부합한다면 '통과',부합하지 않으면 '실패' 라고 출력")
                elif w[0] == '코':
                    code = key
                    code_value = value
                elif w[0] == '실':
                    result = key
                    result_value = value + " 코드를 실행한 결과값 전부를 출력"


        # Bard의 답변을 judgement변수에 담기
        judgement = bard.get_answer(
        f''' 
            {problem} : {problem_value}
            {con} : {con_value}
            {code} : {code_value}
            {result} : {result_value}
        위의 양식에 맞춰 코드를 실행해줘. 그리고 결과를 출력해줄 때 너가 반드시 지켜야할 조건이 있어.
        첫번째, 실행결과값의 첫번째 값 맨 앞에만 '$▶'기호 한개 붙여줘. 다른 값들에겐 이 기호 붙이지 마!.
        두번째, 조건들 중에서 마지막 조건 부합 여부 결과통과 / 실패 의 맨 마지막 뒤에만 '◀$' 기호 한개 붙여줘. 다른 값들에겐 이 기호 붙이지마!.
        '''
        )['content']

        # Bard답변 출력하기
        print(judgement)

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
    # "**실행결과" : 파싱 시작 위치
    a_index = judgement.find("$▶")

    # "end" : 파싱 끝 위치
    b_index = judgement.find("◀$")

    # 파싱 끝낸 결과값 final변수에 담기
    final = judgement[a_index:b_index + 4]
    print("☆파싱 시작-> ", final, " <- 파싱 끝☆")

    # Bard 스크립트가 직접 실행될 때만 main()함수 호출하도록 하는 파이썬의 관례적인 코드
    if __name__ == "__main__":
        main()


    # 채점 결과값 Spring으로 보내기
    # url = "http://localhost:8080/..." # 스프링 엔드포인트(HTTP요청을 처리하는 경로)
    # response = requests.post(url, data=final)
    # print(response.text)


    # 파싱 끝낸 결과값인 final변수 return하기 (가상서버에 출력)
    return final




# Flask객체의 뷰함수 실행
if __name__ == '__main__':
    app.run()