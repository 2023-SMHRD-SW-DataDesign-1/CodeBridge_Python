from flask import Flask, request
from bardapi import BardCookies
from flask_cors import CORS
import json



# Json형태의 데이터 예시 1번
# 문제, 조건들, 학생이 제출한 코드가 Json형태로 변수명 json_data에 담겨져 있다
# json_data = {
#     "문제": "1부터 30까지의 숫자 중 3의 배수를 출력하시오.",
#     "조건1": "1 <= num <= 30",
#     "조건2": "변수명으로 codenum을 사용하시오.",
#     "조건3": "for문과 range함수를 사용하시오.",
#     "조건4" : "if문을 사용하시오.",
#     "코드": """for num in range(3, 31, 3):
#                     print(num),
#                     """
# }


# ========================================================================= # Flask의 함수 시작
# Flask객체를 app변수에 담기
app = Flask(__name__)


# Flask 가상 서버 열기
@app.route('/', methods=['GET', 'POST'])  # URL 설정
def test1():
    
    print('리퀘스트 확인 :', request)

    if (request.method == 'GET'):
        return "GET ok"
    elif (request.method == 'POST'):
        print('리퀘스트 확인1 :', request.get_json())
        # request로 받은 데이터 request_data의 변수에 담기
        request_data = request.get_json()
        print(request_data)


        # json_data의 key의 첫글자에 따라 변수명을 달리하여 key와 value의 값을 담기
        con = []
        con_value = []
        for key, value in request_data.items():
            for w in key:
                if w[0] == 'p':   # problem_content : 문제
                    problem = key
                    problem_value = value
                elif w[0] == 't':   # test_condition : 조건
                    con.append((key))
                    con_value.append(value)
                elif w[0] == 's':   # sub_code : 학생이 제출한 코드
                    code = key
                    code_value = value


    # ========================================================================= # Bard의 함수 시작 : Bard연결,질문,답변

    ## Bard!!! ##
    def getbard():  # Bard API에 연결하기 (쿠기값 = 인증정보)
        cookie_dict = {
            "__Secure-1PSID": "",  # 매번 바뀌므로 주의
            "__Secure-1PSIDTS": "", }  # 매번 바뀌므로 주의

        # Bard_API와 상호작용할 수 있는 객체 만들기 및 인증정보 전달하기
        bard = BardCookies(cookie_dict=cookie_dict)

        # Bard의 답변을 judgement1변수에 담기
        marking = bard.get_answer(
                     f'''
                         {problem} : {problem_value}
                         {code} : {code_value}
                         코드가 실행가능하다면 '정답', 실행불가능하다면 '오답' 이라는 단어로만 답해줘. 그이외의 설명은 하지 말아줘.
                         그리고 답변을 할 때 조건이 있어.
                         답변은 반드시 딕셔너리(dictionary) 형태로 '실행결과' : '정답' 또는 '오답' 이렇게만 출력해줘.
                         (:)콜론을 기준으로 저 2개의 답변 빼고는 어떤 설명도 하지 말아줘.

                     ''')['content']


        marking += bard.get_answer(
                      f'''
                         {con} : {con_value}
                         {code} : {code_value}
                         코드가 각각의 조건에 완벽하게 부합한다면 '통과', 완벽하게 부합하지 않으면 '실패' 라는 단어로만 답해줘. 그이외의 설명은 하지 말아줘.
                         그리고 답변을 할 때 조건이 있어.
                         답변은 반드시 하나의 리스트(list) 형태로 '조건+번호' : '통과' 또는 '실패' 이렇게 각각의 조건부합결과를 하나의 리스트 안에서 쉼표(,)로 구분하여 조건과 결과를 출력해줘.
                         (:)콜론을 기준으로저 2개의 답변 빼고는 어떤 설명도 하지 말아줘.

                     ''')['content']


        # Bard의 답변 출력하고 return하기(Bard함수 실행되면 return함)
        print(marking)
        return marking

    # ========================================================================= # Bard 함수 실행

    # Bard 스크립트의 main함수 정의하기
    def main():
        marking = getbard()
        return marking

    # Bard 스크립트 main함수 실행 및 judgement변수에 담기
    marking = main()

    # Bard 스크립트가 직접 실행될 때만 main()함수 호출하도록 하는 파이썬의 관례적인 코드
    if __name__ == "__main__":
        main()

    # ========================================================================= # Bard함수 실행해서 return받은 답변을 파싱하기

    # Bard의 답변에서 정답과 조건들만 뽑아내기(파싱)
    # 파싱 시작 위치 설정
    a_index = marking.find("{")
    c_index = marking.find("[")

    # 파싱 끝 위치 설정
    b_index = marking.find("}")
    d_index = marking.find("]")

    # 파싱 끝낸 결과값 final변수에 담고 콘솔창에 출력해보기
    final_result = marking[a_index:b_index + 4]
    final_result += marking[c_index:d_index + 4]
    print("☆파싱 시작-> ", final_result, " <- 파싱 끝☆")

    # ========================================================================= #

    # 채점 결과값 Spring으로 보내기
    # url = "http://localhost:8080/..." # 스프링 엔드포인트(HTTP요청을 처리하는 경로)
    # response = requests.post(url, data=final)
    # print(response.text)

    # 파싱 끝낸 결과값인 final변수 return하기 (Flask함수 실행되면 return해서 가상서버에 출력)
    return "null"


# ========================================================================= # Flask 함수 실행

# Flask 실행
if __name__ == '__main__':
    app.run()