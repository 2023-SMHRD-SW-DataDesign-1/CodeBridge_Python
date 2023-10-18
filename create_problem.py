from flask import Flask, request
from bardapi import BardCookies

# 문제 1번
json_data = {
    "문제": "1부터 100까지의 숫자 중 짝수만 출력하시오.",
    "조건1": "1 <= num <= 100",
    "조건2": "if문을 사용하시오.",
    "조건3": " % 연산기호를 사용하시오.",
    "조건4" : "for문을 사용하시오.",
    "코드": """for num in range(3, 31, 3):
                    print(num),                
                    """
}

# Flask객체를 app변수에 담기
app = Flask(__name__)


# Flask 가상 서버 열기
@app.route('/')  # URL 설정
def test1():

    ## Bard!!! ##
    def getbard():  # Bard API에 연결하기 (쿠기값 = 인증정보)
        cookie_dict = {
            "__Secure-1PSID": "cAgpBX3ssxsl18qcr2-Ho0m8XvoNXXyIuwC4gcZXKifsoFctbUwojZXYF-g_o5n_g1ivZQ.",  # 매번 바뀌므로 주의
            "__Secure-1PSIDTS": "sidts-CjIB3e41hRIreEQ5zM5EHIaquNdrH6VqnOaI0RHSsjZdGgk1YUepx-H-bgV9GWlcyRdWIBAA", }  # 매번 바뀌므로 주의

        # Bard_API와 상호작용할 수 있는 객체 만들기 및 인증정보 전달하기
        bard = BardCookies(cookie_dict=cookie_dict)

        # Bard의 답변을 judgement1변수에 담기
        judgement = bard.get_answer(
                    f''' 
                     지금부터 넌 이제 막 코딩을 배우는 학생들을 위해 파이썬 코딩 문제를 출제하는 출제 선생님이야.
                        {{"문제": "1부터 100까지의 숫자 중 짝수만 출력하시오.",
                        "조건1": "1 <= num <= 100",
                        "조건2": "if문을 사용하시오.",
                        "조건3": " % 연산기호를 사용하시오.",
                        "조건4" : "for문을 사용하시오.",
                        "코드": """for num in range(3, 31, 3):
                                        print(num)""",
                        "문제생성" : 생성완료}}
                        반드시 위의 Json형식에 맞춰서 중괄호를 붙여서 코딩 문제를 3개 출제해줘.
                        단, 조건이 있어. 
                        첫번째, json의 중괄호 앞에 '문제1번', '문제2번' 이런식으로 문제 바로 뒤에 띄어쓰지 않고 번호를 매겨서 각각의 문제를 구분해줘.
                        두번째, 조건들은 너가 임의로 랜덤(random)적으로 꼭 지정해줘.
                        세번째, 문제의 난이도는 "상", "중", "하"로 나눠서 "하"에 해당하는 문제 1개, "중"에 해당하는 문제 1개,
                        "상"에 해당하는 문제 1개를 출제해줘. 
                        네번째, 정답인 코드도 '코드' : '정답코드' 이 형식으로 출력해줘.
                        다섯번째, '생성완료1', '생성완료2' 이런식으로 마지막 문제를 출제하고나서 반드시 '생성완료' 뒤에 생성된 문제 번호를 매겨줘.
                        ''')['content']


        # Bard의 답변 출력하고 return하기(Bard함수 실행되면 return함)
        print(judgement)

        # ========================================================================= # Bard함수 실행해서 return받은 답변을 파싱하기

        # Bard의 답변에서 문제들만 뽑아내기(파싱)
        # 파싱 시작 위치 설정
        a_index = judgement.find("문제1번" or "문제 1번")

        # 파싱 끝 위치 설정
        b_index = judgement.find("생성완료5" or "생성완료 5")

        # 파싱 끝낸 결과값 final변수에 담고 콘솔창에 출력해보기
        final = judgement[a_index:b_index + 5]
        print("☆파싱 시작-> ", final, " <- 파싱 끝☆")


        return final


        # ========================================================================= # Bard 함수 실행


    # Bard 스크립트의 main함수 정의하기
    def main():
        final = getbard()
        return final

    # Bard 스크립트 main함수 실행 및 judgement변수에 담기
    final = main()

    # Bard 스크립트가 직접 실행될 때만 main()함수 호출하도록 하는 파이썬의 관례적인 코드
    if __name__ == "__main__":
        main()


    return final


# ========================================================================= # Flask 함수 실행

# Flask 실행
if __name__ == '__main__':
    app.run()