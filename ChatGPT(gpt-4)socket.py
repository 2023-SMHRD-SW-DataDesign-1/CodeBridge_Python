from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ChatGPT API 키 설정
os.environ['OPENAI_API_KEY'] = ""

llm = ChatOpenAI(
    temperature=0.3,
    max_tokens=800,
    model_name='gpt-4',
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

@app.route("/")
def index():
    return "WebSocket server is running."

@socketio.on('message')
def handle_message(data):
    request_data = data.get('request_data')
    problem_content = request_data.get("test_contents")
    sub_code = request_data.get("sub_code")
    test_conditions = request_data.get("test_conditions")

    question = f'''
        - 문제 : {problem_content},
        - 테스트케이스 내용 : {test_conditions},
        - 학생이 제출한 코드 : {sub_code}
        '문제'를 읽고 '테스트케이스의 내용'을 기준으로 '학생이 제출한 코드'가 '테스트케이스의 각각의 내용'에 부합하는지 채점해주세요.
         테스트케이스의 내용에는 각각 번호가 매겨져있습니다. 번호별로 판단해서 학생이 제출한 코드가 테스트케이스의 내용 중 하나의 요소에 부합할 때마다 "테스트케이스+번호: 성공"이라고 출력해주세요.
         번호별로 판단해서 테스트케이스의 내용 중 하나의 요소에 부합하지 않을 때마다 "테스트케이스+번호: 실패"라고 출력해주세요.
         테스트케이스의 판단결과의 이유를 한 줄로 짧게 50자 이내로 설명해주세요.
         '''
    response = llm.predict(question)


    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)

