from flask import Flask, request
from bardapi import BardCookies

# 문제 1번
# json_data = {
#     "문제": "1부터 100까지의 숫자 중 짝수만 출력하시오.",
#     "조건1": "1 <= num <= 100",
#     "조건2": "if문을 사용하시오.",
#     "조건3": " % 연산기호를 사용하시오.",
#     "조건4" : "for문을 사용하시오.",
#     "코드": """for num in range(3, 31, 3):
#                     print(num),
#                     """
# }

# Flask객체를 app변수에 담기
app = Flask(__name__)


# Flask 가상 서버 열기
@app.route('/')  # URL 설정
def test1():

    # Bard에 연결하기
    cookie_dict = {
        "__Secure-1PSID": "cAgpBX3ssxsl18qcr2-Ho0m8XvoNXXyIuwC4gcZXKifsoFctbUwojZXYF-g_o5n_g1ivZQ.",  # 매번 바뀌므로 주의
        "__Secure-1PSIDTS": "sidts-CjIB3e41hTgIRD23jmMuewPfsVbtYmsAu6iJOYM2usGsS9lnhRFPb_xchOBCuyLgcgCSzhAA", }  # 매번 바뀌므로 주의

    # Bard_API와 상호작용할 수 있는 객체 만들기
    bard = BardCookies(cookie_dict=cookie_dict)

    # Bard에게 질문하고 답변을 bard_answer변수에 담기
    bard_answer = bard.get_answer(
                ''' 
                 지금부터 넌 이제 막 코딩을 배우는 학생들을 위해 파이썬 코딩 문제를 출제하는 출제 선생님이야.
                    {{"문제": "1부터 100까지의 숫자 중 짝수만 출력하시오.",
                    "조건1": "1 <= num <= 100",
                    "조건2": "if문을 사용하시오.",
                    "조건3": " % 연산기호를 사용하시오.",
                    "조건4" : "for문을 사용하시오.",
                    "코드": """for num in range(3, 31, 3):
                                    print(num)""",
                    }}
                    
                위의 출제 형식을 보고 새로운 유형의 문제를 난이도를 '상, 중, 하'로 나눠 각각 3개씩 만들어서 총 18개의 문제를 생성해줘.
                단, 답변할 때 조건이 있어.
                첫번째, 반드시 JSON형식에 맞춰서 각각의 문제를 출제해줘.
                두번째, 오로지 문제1번 앞에만 << 이 기호를 반드시 붙여줘.
                세번째, 오로지 문제18번 끝에만 >> 이 기호를 반드시 붙여줘.   
                    ''')['content']


    # Bard의 답변 출력하기
    print(bard_answer)

    # Bard의 답변에서 문제들만 뽑아내기(파싱)
    # 파싱 시작 위치 설정
    start_index = bard_answer.find("<<")

    # 파싱 끝 위치 설정
    end_index = bard_answer.find(">>")

    # 파싱을 끝낸 최종 결과값 parse_result변수에 담고 콘솔창에 출력해보기
    parse_result = bard_answer[start_index : end_index + 2]
    print("파싱된 최종결과 :", parse_result)

    # 파싱된 최종 결과값 return하기
    return parse_result


# Flask 실행
if __name__ == '__main__':
    app.run()