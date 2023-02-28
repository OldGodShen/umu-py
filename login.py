import requests
username=input("输入账号")
passwd=input("输入密码")

url = "https://m.umu.cn/passport/ajax/account/login"

payload = "username=" + username + "&passwd=" + passwd
headers = {"content-type": "application/x-www-form-urlencoded"}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)