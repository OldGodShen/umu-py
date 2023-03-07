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

def loginF(username,passwd):

    url = "https://m.umu.cn/passport/ajax/account/login"

    payload = "username=" + username + "&passwd=" + passwd
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    umuU = response.cookies["umuU"]
    JSESSID = response.cookies["JSESSID"]
    return umuU,JSESSID

def getanswer(element_id,question_ids):

    umuU,JSESSID = loginF("jtabm34","123456")

    url = "https://m.umu.cn/napi/v1/quiz/question-right-answer"

    querystring = {"_type":"1","element_id":"" + element_id + "","question_ids":"" + question_ids + ""}

    headers = {"Cookie": "umuU="+ umuU + ";JSESSID=" + JSESSID}

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_dict = json.loads(response.text)

    rightanswer_data = response_dict['data']

    for rightanswer_key,rightanswer_value in rightanswer_data.items():
        for rightanswer_values in rightanswer_value[0]:
            for rightanswer_values_type,rightanswer_values_answer in rightanswer_values:
                answer_ids = []
                if rightanswer_values_type == "right_answer_id":
                    answer_ids.append(rightanswer_values_answer)
                    if len(rightanswer_values) == 1:
                        answer_type = "radio"
                    else:
                        answer_type = "checkbox"
                elif rightanswer_values_type == "right_answer_content":
                    content = rightanswer_values_answer
                    answer_type = "input"
        answer = []
        if answer_type == "radio":
            answer.append({"type":"radio","question_id":rightanswer_key,"answer_ids":answer_ids,"content":"","level":2})
        elif answer_type == "checkbox":
            answer.append({"type":"checkbox","question_id":rightanswer_key,"answer_ids":answer_ids,"content":"","level":2})
        elif answer_type == "input":
            answer.append({"type":"input","question_id":rightanswer_key,"answer_ids":"[]","content":"" + content + "","level":2})
            

        
