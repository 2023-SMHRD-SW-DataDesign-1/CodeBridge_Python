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
@app.route("/mark", methods=['GET', 'POST'])  # URL 설정
def test1():
    # 받은 데이터 각각 변수에 담기
    if (request.method == 'GET'):
        return "GET ok"
    elif (request.method == 'POST'):
        request_data = request.get_json()
        print('request_data확인', request_data)
        # problem_content : 문제
        problem_content = request_data.get("test_contents")
        # sub_code : 학생이 제출한 코드
        sub_code = request_data.get("sub_code")
        # test_conditions = 문제의 조건
        test_conditions = request_data.get("test_conditions")



    # => ChatGPT 연결하기
    # ChatGPT_API키 입력하기
    os.environ['OPENAI_API_KEY'] = ""


    # 객체 생성하고 옵션 설정하기
    llm = ChatOpenAI(temperature=0.1,                           # temperature : 창의성 (0.0 ~ 2.0) 사이로 설정 가능.
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
         테스트케이스의 내용에는 각각 번호가 매겨져있습니다. 번호별로 판단해서 학생이 제출한 코드가 테스트케이스의 내용에 부합한다면 
         "테스트케이스+번호: 성공" 부합하지 않는다면 "테스트케이스+번호: 실패"라고 출력, 판단결과의 이유를 줄바꿈 한 후 한 줄로 짧게 50자 이내로 "이유:"라고 설명해주세요.
         '''

    # 답변(스트리밍X) 출력하기
    # print(f'[GPT답변]: {llm.predict(question)}')

    # 스트리밍으로 답변 출력하기
    response = llm.predict(question)




    # Flask함수의 return값
    return response


@app.route("/test", methods=['GET', 'POST'])  # URL 설정
def test2():
    # => ChatGPT 연결하기
    # ChatGPT_API키 입력하기
    os.environ['OPENAI_API_KEY'] = ""

    # 객체 생성하고 옵션 설정하기
    llm = ChatOpenAI(temperature=0.3,  # temperature : 창의성 (0.0 ~ 2.0) 사이로 설정 가능.
                     max_tokens=800,  # max_tokens : 최대 토큰수
                     model_name='gpt-4',  # model_name : 모델명
                     streaming=True,  # streaming : 실시간으로 답변받기
                     callbacks=[StreamingStdOutCallbackHandler()]
                     )

    # 질의 내용 작성하기
    question = '''
                지금부터 당신은 이제 막 코딩을 배우는 학생들을 위해 자바(Java) 코딩 문제를 출제하는 출제 선생님입니다.
                예시에 맞춰 문제를 출제해주세요.
                단, 답변할 때 조건이 있습니다. 아래의 제시된 조건에 맞춰 1문제만 출제해 주십시오.
                {
                테스트 제목 : 
                문제 : 
                테스트케이스n번 :  
                테스트케이스n+1번 :  
                .... , 
                } 이 형식을 지켜주세요.

                아래에 5개의 예시를 적어놓겠습니다. 참고하여 문제를 출제해주세요.

                (1번 예시)
                테스트 제목 : 문자열 제거하기
                문제 : `"HelloWorld" 라는 문자열 str이 주어질 때, str을 출력하는 코드를 작성해 보세요.
                테스트케이스1. str변수에 "HelloWorld"문자열을 대입하기
                테스트케이스2. 출력함수 사용하기
                테스트케이스3. 코드를 컴파일 해서 결과값으로 "HelloWorld" 를 출력하기

                (2번 예시)
                테스트 제목 : 문자열 배열로 만들기
                문제 : 단어가 공백 한 개 이상으로 구분되어 있는 문자열 "I love you"가 주어질 때, "I love you"에서 공백으로 단어를 구분하여 나온 단어를 앞에서부터 순서대로 담은 문자열 배열을 출력하시오.
                테스트케이스1. str변수에 "I love you"문자열을 대입하기
                테스트케이스2. split()함수를 사용하여 코드를 작성하기
                테스트케이스3. for문을 사용하여 코드를 작성하기
                테스트케이스4. 코드를 컴파일 해서 결과값으로 ["I", "love", "you"] 를 출력하기

                (3번 예시)
                테스트 제목 : 배열 합 구하기
                문제 : 주어진 정수 배열의 모든 요소의 합을 구하는 코드를 작성해보세요.
                                        ex) 정수 배열
                                        int[] arr = {5, 8, 2, 10, 7};
                테스트케이스1. 1차원 배열 사용하여 코드 작성하기
                테스트케이스2. for문을 사용하여 코드를 작성하기
                테스트케이스3. 코드를 컴파일 해서 결과값이 32 가 출력하기

                (4번 예시)
                테스트 제목 : 최대값, 최소값 구하기
                문제 : 주어진 숫자 배열에서 가장 큰 숫자와 가장 작은 숫자의 차이를 구하는 프로그램을 작성하시오.
                                        ex)
                                        int [ ] numbers = {1, 10, 2, 9, 3, 8, 4, 7, 5, 6};
                테스트케이스1. 1차원 배열 사용하여 코드 작성하기
                테스트케이스2. 최소값과 최대값의 초기값을 담는 변수의 이름을 small과 large로 사용하기
                테스트케이스3. if문을 사용하여 코드를 작성하기
                테스트케이스4. 코드를 컴파일 해서 결과값으로 9 가 출력하기

                (5번 예시)
                테스트 제목 : 공백 제거하기
                문제 : "Hello, world!" 문자열에서 공백을 제거하는 프로그램을 작성하시오.
                테스트케이스1. "Hello, world!"라는 문자열을 str이라는 변수에 담기
                테스트케이스2. replace()함수를 사용하여 공백을 제거하기
                테스트케이스3. 코드를 컴파일 해서 결과값으로  "Hello,world!" 를 출력하기
                '''

    # 답변(스트리밍X) 출력하기
    # print(f'[GPT답변]: {llm.predict(question)}')

    # 스트리밍으로 답변 출력하기
    response = llm.predict(question)

    # # ChatGPT의 답변을 파싱하기
    # start_index = response.find("문제시작")
    # end_index = response.find("문제완료")
    #
    # parse_result = []
    # parse_result.append(response[start_index: end_index + 4])
    #
    # # 파싱된 결과 출력하기
    # print("\n", "&& 파싱된 최종 결과 && :", parse_result)

    # Flask함수의 return값
    return response


# Flask 실행
if __name__ == '__main__':
    app.run()
