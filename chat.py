import openai
import time

# OPENAI API 키 입력


messages = [
    {"role" : "system", "content" : "너는 단답형 채점기야"}
]

start = time.time()

content = '''
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
'''
print("content : ", content)

messages.append({"role" : "user", "content" : content})

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

chat_response = completion.choices[0].message.content
print(f'ChatGPT : {chat_response}')