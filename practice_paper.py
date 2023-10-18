# json_data = {
#     "문제": "1부터 30까지의 숫자 중 3의 배수를 출력하시오.",
#     "조건1": "1 <= num <= 30",
#     "조건2": "변수명으로 num을 사용하시오.",
#     "조건3": "for문과 range함수를 사용하시오.",
#     "실행결과" : "null",
#     "코드": """for num in range(3, 31, 3):
#                     print(num),
#                     """
# }
#
# # for key, value in json_data.items():
# #     for w in key:
# #         if w[0] == "문":
# #             print(key)
# #             print(value, "이 값은 출력하지 말아주세요1.")
# #         elif w[0] == "코":
# #            print(key)
# #            print(value)
# #         elif w[0] == "실":
# #             print(key)
# #             print(value, "코드의 실행 결과값 전부를 출력")
# #         elif w[0] == "조":
# #             print(key)
# #             print(value, "해당 조건에 만족하면 <통과>, 만족하지않으면 <실패> 출력")
#
#
# con = []
# con_value = []
# for key, value in json_data.items():
#     for w in key:
#         if w[0] == '문':
#             problem = key
#             problem_value = value
#         elif w[0] == '조':
#             con.append((key))
#             con_value.append(value + " 해동 조건에 부합하면 <통과>, 부합하지 않으면 <실패> 출력")
#         elif w[0] == '코':
#             code = key
#             code_value = value
#         elif w[0] == '실':
#             result = key
#             result_value = value + " 코드를 실행한 결과값 전부를 출력"
#
#
# print(con[0])
# print(con_value[0])
# print(problem_value)
# print(code)
# print(result_value)


#
# json_data = {
#     "문제": "1부터 30까지의 숫자 중 3의 배수를 출력하시오.",
#     "조건1": "1 <= num <= 30",
#     "조건2": "변수명으로 num을 사용하시오.",
#     "조건3": "for문과 range함수를 사용하시오.",
#     "실행결과" : "null",
#     "코드": """for num in range(3, 31, 3):
#                     print(num)"""
#  }
#
#
# input_variables_list = []
# for key,value in json_data.items():
#     input_variables_list.append(key)
# print(input_variables_list)




