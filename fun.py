import requests
import json

def login(username,passwd):

    url = "https://m.umu.cn/passport/ajax/account/login"

    payload = "username=" + username + "&passwd=" + passwd
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)
    response_dict = json.loads(response.text)

    student_id = response_dict['data']['user_info']['student_id']
    umuU = response.cookies["umuU"]
    JSESSID = response.cookies["JSESSID"]
    return student_id,umuU,JSESSID

def getanswer():

    url = "https://m.umu.cn/napi/v1/quiz/question-right-answer"

    querystring = {"_type":"1","element_id":"{{element_id}}","question_ids":"{{question_id}}"}

    headers = {"Cookie": "umuU={{FumuU}};JSESSID={{FJSESSID}}"}

    response = requests.request("GET", url, headers=headers, params=querystring)