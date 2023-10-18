from flask import Flask, request
from bardapi import BardCookies
from flask_cors import CORS
import re
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
        request_data = request.get_json()
        print("되라!!", request_data)

        # json_data의 key의 첫글자에 따라 변수명을 달리하여 key와 value의 값을 담기
        con = []
        con_value = []
        for key, value in request_data.items():
            for w in key:
                if w[0] == 'p':  # problem_content : 문제
                    problem = key
                    problem_value = value
                elif w[0] == 't':  # test_condition : 조건
                    con.append((key))
                    con_value.append(value)
                elif w[0] == 's':  # sub_code : 학생이 제출한 코드
                    code = key
                    code_value = value

            # ========================================================================= # Bard의 함수 시작 : Bard연결,질문,답변

            ## Bard!!! ##

        def getbard():  # Bard API에 연결하기 (쿠기값 = 인증정보)
            cookie_dict = {
                "__Secure-1PSID": "bwjEVU5yMQRiIn298__CQ7AbojY9zADKOWtZo0UiMsVndzfonxrCxuuOuF_4DkY_moMMKA.",
                # 매번 바뀌므로 주의
                "__Secure-1PSIDTS": "sidts-CjIB3e41hbhEBuZqaLGDDow5taWHFRRhndI06r5y1lcV6wvyUq4LQbs8buODA5hF0__hGRAA", }  # 매번 바뀌므로 주의

            # Bard_API와 상호작용할 수 있는 객체 만들기 및 인증정보 전달하기
            bard = BardCookies(cookie_dict=cookie_dict)

            # Bard의 답변을 judgement1변수에 담기
            marking1 = bard.get_answer(
                f''' 
                문제 :
                {problem_value}
                제출한 코드 :
                {code_value}
                제한조건 :
                {con_value}
                
                1번 2번 문장으로만 답변해줘, 
                1, 2번 문장 이외의 답변은 절대 하지마,
                1번 답변은 <<<>>> 로 감싸주고 2번 답변은 !!! 로 감싸줘
                다른말, 설명은 절대 하지마
                1. 제출한 코드가 문제에 대해 => <<<정답 or 오답>>>
                2. 조건n 번이 제출한 코드가 제한조건에 => !!!n번 조건 : 만족 or 불만족!!!
                            ''')['content']



            # Bard의 답변 출력하고 return하기(Bard함수 실행되면 return함)
            # print(marking1)
            return marking1

            # ========================================================================= # Bard 함수 실행

            # Bard 스크립트의 main함수 정의하기

            # Bard 스크립트 main함수 실행 및 judgement변수에 담기


        # Bard 스크립트가 직접 실행될 때만 main()함수 호출하도록 하는 파이썬의 관례적인 코드
        if __name__ == "__main__":
            marking = getbard()
            print('마킹', marking)

        # ========================================================================= # Bard함수 실행해서 return받은 답변을 파싱하기

        # # Bard의 답변에서 정답과 조건들만 뽑아내기(파싱)
        # # 파싱 시작 위치 설정
        # a_index = marking.find("<<<")
        # c_index = marking.find(">>>")
        #
        # # 파싱 끝 위치 설정
        # b_index = marking.find("!!!")
        # d_index = marking.find("!!!")
        #
        # # 파싱 끝낸 결과값 final변수에 담고 콘솔창에 출력해보기
        # final_result = marking[a_index:b_index + 4]
        # final_result += marking[c_index:d_index + 4]
        # print("☆파싱 시작-> ", final_result, " <- 파싱 끝☆")

        def parse_marking(marking):
            # 각 정보를 추출하는 정규 표현식
            pattern = r'(\d+|\d+\.)\. ([^!]+) <<<([^>]+)>>>|\d+\. ([^!]+) !!!\[([^\]]+)\]!!!'

            matches = re.finditer(pattern, marking)
            results = []

            for match in matches:
                groups = match.groups()
                if groups[0]:  # 정답 정보
                    results.append(('정답', groups[2]))
                else:  # 조건 정보
                    results.append((f'조건{groups[3]}', groups[4].strip()))

            return results

        results = parse_marking(marking)
        print('results 확인', results)

        # ========================================================================= #

        # 채점 결과값 Spring으로 보내기
        # url = "http://localhost:8080/..." # 스프링 엔드포인트(HTTP요청을 처리하는 경로)
        # response = requests.post(url, data=final)
        # print(response.text)

        # 파싱 끝낸 결과값인 final변수 return하기 (Flask함수 실행되면 return해서 가상서버에 출력)


        return final_result







# Flask 실행
if __name__ == '__main__':
    app.run()
