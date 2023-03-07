import requests
Fusername="jtabm34"
Fpasswd="123456"

url = "https://m.umu.cn/passport/ajax/account/login"

payload = "username=" + Fusername + "&passwd=" + Fpasswd
headers = {"content-type": "application/x-www-form-urlencoded"}

response = requests.request("POST", url, data=payload, headers=headers)

url = "https://m.umu.cn/napi/v1/quiz/question-right-answer"

querystring = {"_type":"1","element_id":"{{element_id}}","question_ids":"{{question_id}}"}

headers = {"Cookie": "umuU={{FumuU}};JSESSID={{FJSESSID}}"}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)