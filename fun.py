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

    answer = []
    for rightanswer_key,rightanswer_value in rightanswer_data.items():
        for rightanswer_values_type,rightanswer_values_right in rightanswer_value[0].items():
            answer_ids = []
            if rightanswer_values_type == "right_answer_id":
                answer_ids.append(rightanswer_values_right)
                if len(rightanswer_value[0]) == 1:
                    answer_type = "radio"
                else:
                    answer_type = "checkbox"
            elif rightanswer_values_type == "right_answer_content":
                content = rightanswer_values_right
                answer_type = "input"
        if answer_type == "radio":
            answer.append({"type":"radio","question_id":int(rightanswer_key),"answer_ids":answer_ids,"content":"","level":2})
        elif answer_type == "checkbox":
            answer.append({"type":"checkbox","question_id":int(rightanswer_key),"answer_ids":answer_ids,"content":"","level":2})
        elif answer_type == "input":
            answer.append({"type":"input","question_id":int(rightanswer_key),"answer_ids":"[]","content":"" + content + "","level":2})
    answer_json = json.dumps(answer)
    return answer_json

def getanswertext(answertext):

    response_dict = json.loads(answertext)

    rightanswer_data = response_dict['data']

    answer = []
    for rightanswer_key,rightanswer_value in rightanswer_data.items():
        for rightanswer_values_type,rightanswer_values_right in rightanswer_value[0].items():
            answer_ids = []
            if rightanswer_values_type == "right_answer_id":
                answer_ids.append(rightanswer_values_right)
                if len(rightanswer_value[0]) == 1:
                    answer_type = "radio"
                else:
                    answer_type = "checkbox"
            elif rightanswer_values_type == "right_answer_content":
                content = rightanswer_values_right
                answer_type = "input"
        if answer_type == "radio":
            answer.append({"type":"radio","question_id":int(rightanswer_key),"answer_ids":answer_ids,"content":"","level":2})
        elif answer_type == "checkbox":
            answer.append({"type":"checkbox","question_id":int(rightanswer_key),"answer_ids":answer_ids,"content":"","level":2})
        elif answer_type == "input":
            answer.append({"type":"input","question_id":int(rightanswer_key),"answer_ids":"[]","content":"" + content + "","level":2})
    answer_json = json.dumps(answer)
    return answer_json
            
def startexam(element_id,exam_submit_id,umuU,JSESSID):
    url = "https://m.umu.cn/megrez/exam/v1/startExam"

    payload = "session_id=" + element_id + "&student_id=0&exam_submit_id=" + exam_submit_id
    headers = {
        "Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID,
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)