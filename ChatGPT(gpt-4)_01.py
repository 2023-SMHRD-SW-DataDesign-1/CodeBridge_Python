### <LangChain 사용> ###

# => 필요한 라이브러리 설치하기

# ChatGPT를 사용하기 위한 API_KEY입력을 위한 라이브러리
import os

# LangChain에서 ChatGPT를 사용하기 위한 라이브러리
from langchain.chat_models import ChatOpenAI

# GPT의 답변 실시간으로 받기 위한 라이브러리
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Flask서버와 서버를 통해 데이터 받기 위한 라이브러리
from flask import Flask, request

# Flask서버에서 생길 수 있는 오류 해결하기 위한 라이브러리
from flask_cors import CORS

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

        # problem_content : 문제
        problem_content = request_data.get("test_contents")
        # sub_code : 학생이 제출한 코드
        sub_code = request_data.get("sub_code")
        # test_conditions = 문제의 조건
        test_conditions = request_data.get("test_condition")


    # => ChatGPT 연결하기
    # ChatGPT_API키 입력하기
    os.environ['OPENAI_API_KEY']= "xxx"


    # 객체 생성하고 옵션 설정하기
    llm = ChatOpenAI(temperature=0.3,                           # temperature : 창의성 (0.0 ~ 2.0) 사이로 설정 가능.
                     max_tokens=800,                          # max_tokens : 최대 토큰수
                     model_name='gpt-4',              # model_name : 모델명
                     streaming=True,                          # streaming : 실시간으로 답변받기
                     callbacks=[StreamingStdOutCallbackHandler()]
                     )

    # 질의 내용 작성하기
    question = f'''
        - 문제 : {problem_content},
        - 테스트케이스 내용 : {test_conditions},
        - 학생이 제출한 코드 : {sub_code}
    
        '문제'를 읽고 '테스트케이스의 내용'을 기준으로 '학생이 제출한 코드'가 '테스트케이스의 각각의 내용'에 부합하는지 채점해주세요.
         테스트케이스의 내용에는 각각 번호가 매겨져있습니다. 번호별로 판단해서 학생이 제출한 코드가 테스트케이스의 내용 중 하나의 요소에 부합할 때마다 "테스트케이스+번호: 10점 획득"이라고 출력해주세요.
         번호별로 판단해서 테스트케이스의 내용 중 하나의 요소에 부합하지 않을 때마다 "테스트케이스+번호: 점수획득실패"라고 출력해주세요.
         테스트케이스의 판단결과의 이유를 한 줄로 짧게 50자 이내로 설명해주세요.
         마지막에는 출력된 테스트케이스의 판단결과를 모아서 "<< >>" 이 기호 안에 넣어 출력해주세요. 
         (예시) <<테스트케이스1: 10점 획득, 테스트케이스2: 점수획득 실패,...>>)
         '''

    # 답변(스트리밍X) 출력하기
    # print(f'[GPT답변]: {llm.predict(question)}')

    # 스트리밍으로 답변 출력하기
    response = llm.predict(question)

    # ChatGPT의 답변을 파싱하기
    start_index = response.find("<<")
    end_index = response.find(">>")

    parse_result = []
    parse_result.append(response[start_index: end_index + 2])

    # 파싱된 결과 출력하기
    print("\n", "&& 파싱된 최종 결과 && :", parse_result)


    # Flask함수의 return값
    return "ok"


# Flask 실행
if __name__ == '__main__':
    app.run()
