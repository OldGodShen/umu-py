import requests
username=input("输入账号")
passwd=input("输入密码")

url = "https://m.umu.cn/napi/v1/quiz/question-right-answer"

querystring = {"_type":"1","element_id":"{{element_id}}","question_ids":"{{question_id}}"}

headers = {"Cookie": "umuU={{FumuU}};JSESSID={{FJSESSID}}"}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)