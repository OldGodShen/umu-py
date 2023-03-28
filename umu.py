import requests
import json
from bs4 import BeautifulSoup
import time
requests.packages.urllib3.disable_warnings()

def login(username,passwd):

    url = "https://m.umu.cn/passport/ajax/account/login"

    payload = "username=" + username + "&passwd=" + passwd
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)
    response_dict = json.loads(response.text)

    if response_dict['error_code'] == 20001:
        exit("请输入至少6位密码，区分大小写")
    elif response_dict['error_code'] == -1:
        exit("账户与密码不一致")
    elif response_dict['error_code'] == 0:
        student_id = response_dict['data']['user_info']['student_id']
        umuU = response.cookies["umuU"]
        JSESSID = response.cookies["JSESSID"]
        return student_id,umuU,JSESSID
    else:
        exit("未知错误")

def getanswer(username,passwd,element_id,question_ids):

    student_id,umuU,JSESSID = login(username,passwd)
    url = "https://m.umu.cn/napi/v1/quiz/question-right-answer"

    querystring = {"_type":"1","element_id":element_id,"question_ids":question_ids}

    headers = {"Cookie": "umuU="+ umuU + ";JSESSID=" + JSESSID}

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_dict = json.loads(response.text)
    try:
        rightanswer_data = response_dict['data']
    except:
        exit("获取答案失败")

    try:
        answer = []
        for rightanswer_key,rightanswer_value in rightanswer_data.items():
            answer_ids = []
            for rightanswer_values in rightanswer_value:
                for rightanswer_values_type,rightanswer_values_right in rightanswer_values.items():
                    if rightanswer_values_type == "right_answer_id":
                        answer_ids.append(rightanswer_values_right)
                        if len(rightanswer_value) == 1:
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
                answer.append({"type":"input","question_id":int(rightanswer_key),"answer_ids":[],"content":"" + content + "","level":2})
        answer_json = json.dumps(answer)
        print("从已完成用户获取答案成功")
        return answer_json
    except:
        exit("解析答案失败")
            
def startexam(umuU,JSESSID,element_id,student_id,exam_submit_id):
    url = "https://m.umu.cn/megrez/exam/v1/startExam"

    payload = "session_id=" + str(element_id) + "&student_id=" + str(student_id) + "&exam_submit_id=" + str(exam_submit_id)
    headers = {
        "Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID,
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response_dict = json.loads(response.text)

    try:
        start_time = response_dict['data']['time_setting']['start_time_stamp']
        return start_time
    except:
        exit("开始考试错误")

def saveanswer(umuU,JSESSID,element_id,answerlist,student_id,exam_submit_id):
    url = "https://m.umu.cn/megrez/exam/v1/saveAnswer"

    payload = "session_id=" + str(element_id) + "&answer_list=" + str(answerlist) + "&student_id=" + str(student_id) + "&exam_submit_id=" + str(exam_submit_id)
    headers = {
        "Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID,
        "content-type": "application/x-www-form-urlencoded"
    }
    
    try:
        requests.request("POST", url, data=payload, headers=headers)
    except:
        exit("保存答案错误")

def endexam(umuU,JSESSID,element_id,student_id,exam_submit_id):
    url = "https://m.umu.cn/megrez/exam/v1/submitExam"

    payload = "session_id=" + str(element_id) + "&status=2&name=&submit_type=2&student_id=" + str(student_id) + "&exam_submit_id=" + str(exam_submit_id)
    headers = {
        "Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID,
        "content-type": "application/x-www-form-urlencoded"
    }

    time.sleep(5)

    try:
        requests.request("POST", url, data=payload, headers=headers)
    except:
        exit("上传答案错误")

def getexamid(umuU,JSESSID,quiz):
    url = "https://m.umu.cn/session/quiz/" + quiz

    headers = {"Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID}

    response = requests.request("GET", url, headers=headers)

    script = BeautifulSoup(response.text,'lxml')
    pagedata_begin = str(script.html.script).replace("<script>var pageData=","")
    pagedata_end_loc = pagedata_begin.find('QuizSuccess"}')
    if pagedata_end_loc != -1:
        pagedata_end_loc = pagedata_end_loc + 13
    else:
        pagedata_end_loc = pagedata_begin.find('quiz"}')
        if pagedata_end_loc != -1:
            pagedata_end_loc = pagedata_end_loc + 7
        else:
            pagedata_end_loc = pagedata_begin.find('_dwt":"exam"') + 13
    
    try:
        pagedata = json.loads(pagedata_begin[0:pagedata_end_loc])
        element_id = int(pagedata['data']['quizLegacyData']['session_info']['sessionId'])
        exam_submit_id = pagedata['data']['exam_submit_id']
    except:
        exit("获取考试号错误/获取考试提交号错误")

    return element_id,exam_submit_id

def retakeexam(umuU,JSESSID,element_id):
    url = "https://m.umu.cn/api/exam/takeexamagain"

    payload = "session_id=" + str(element_id)
    headers = {
        "Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID,
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    
    try:
        json.loads(response.text)
    except:
        exit("重新开始考试错误")

def getquestionlist(umuU,JSESSID,element_id):
    url = "https://m.umu.cn/napi/v1/quiz/question-list"

    querystring = {"_type":"1","element_id":element_id,"page":"1","size":"100"}

    headers = {"Cookie": "umuU=" + umuU + ";JSESSID=" + JSESSID}

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        response_dict = json.loads(response.text)
        list = response_dict['data']['list']
        questionlist = []
        for question in list:
            questionlist.append(question['id'])
        questionlist_str = str(questionlist)[1:-1]
        questionlist_str = questionlist_str.replace(" ","")
        return questionlist_str
    except:
        exit("获取问题列表错误")

def getanswerfromgithub_shen(element_id):
    url = "https://raw.githubusercontent.com/OldGodShen/umu-json/main/" + str(element_id) + ".json"

    try:
        response = requests.request("GET", url, verify=False)
        print("从GitHub获取答案成功")
        return response.text
    except:
        print("从GitHub获取答案失败，正在从Gitee镜像仓库获取")
        return getanswerfromgitee_shen(element_id)

def getanswerfromgitee_shen(element_id):
    url = "https://gitee.com/OldGodShen/umu-json/raw/main/" + str(element_id) + ".json"

    response = requests.request("GET", url)
    return response.text
