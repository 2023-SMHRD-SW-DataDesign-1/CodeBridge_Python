import openai
from flask import Flask, request
from flask_cors import CORS
import json



# OpenAI객체 생성
completion = openai.Completion

# 연결 설정
# OpenAI config
temperature = 1.0
# 생성되는 텍스트의 창의성 제어 (값이 높을수록 창의적)
top_p = 1.0
# 생성되는 텍스트의 다양성 제어 (값이 높을수록 다양)
best_of = 1
# 생성되는 텍스트의 횟수 제어 (1인경우 한번만, 10이면 열번 생성)
frequency_penalty = 0.0
# 생성되는 텍스트의 빈도 제어 (값이 높을수록 더 드문 단어 사용)
presence_pentaly = 0.5
# 생성되는 텍스트의 존재감 제어 (값이 높을수록 더 많은 단어 사용)

# load API key
openai.api_key = "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"

# prompt 작성
prompt =  '''
            지금부터 넌 이제 막 코딩을 배우는 학생들을 위해 파이썬 코딩 문제를 출제하는 출제 선생님이야.
            난이도를 '상, 중, 하'로 나눠서 난이도별로 각각 1개씩 출제해줘.
            단, 답변할 때 조건이 있어.
            첫번째, 반드시 JSON형식에 맞춰 중괄호 안에 담아서 각각의 문제를 출제해줘.
            두번째, 문제의 내용도 문제마다 달리하여 겹치지 않게 다양하게 만들어줘.
            세번째, {문제 : , 
                    조건n번 : , 
                    조건n번 : , 
                    .... , 
                    정답코드 : } 이 형식을 바탕으로 문제를 새롭게 생성해줘.
            네번째, 조건의 번호인 n은 1~4 사이의 숫자를 사용할 수 있어.
            문제를 하나씩 출제할 때마다 조건의 갯수를 달리해서 파이썬 코딩 문제를 출제해줘.
            '''

# API 호출
def ask_for_short_answer(prompt):
    response = completion.create(
        prompt=prompt,
        # 생성할 초기 텍스트
        model="text-davinci-003",
        # 사용할 모델
        max_tokens=1500,
        # 생성할 텍스트의 최대 토큰 수 (1토큰=1개의 단어 또는 구)
        temperature=temperature,
        top_p=top_p,
        best_of=best_of,
    )

    return response.choices[0].text.strip()

result = ask_for_short_answer(prompt)
print(result)
