import requests
import json
username=input("输入账号:")
passwd=input("输入密码:")

url = "https://m.umu.cn/passport/ajax/account/login"

payload = "username=" + username + "&passwd=" + passwd
headers = {"content-type": "application/x-www-form-urlencoded"}

response = requests.request("POST", url, data=payload, headers=headers)
response_dict = json.loads(response.text)

if response_dict['error_code'] == 20001:
    print("请输入至少6位密码，区分大小写")
elif response_dict['error_code'] == -1:
    print("账户与密码不一致")
elif response_dict['error_code'] == 0:
    student_id = response_dict['data']['user_info']['student_id']
    print("student_id:" + student_id)
    umuU = response.cookies["umuU"]
    print("umuU:" + umuU)
    JSESSID = response.cookies["JSESSID"]
    print("JSESSID:" + JSESSID)
else:
    print("未知错误")