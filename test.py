import umu

u = input("输入用户名:")
p = input("输入密码:")
print("正在尝试登录")
s,u,J = umu.login(u,p)

quiz = input("输入考试地址:")
print("正在获取考试号")
e,ex = umu.getexamid(u,J,quiz)

while True:
    try:
        way = int(input("使用GitHub/Gitee上的OldGodShen/umu-json答案库(0),使用已完成账号获取答案(1):"))
        if way == 0 or way == 1:
            break
        else:
            print("目前没有该选项")
    except:
        print("请输入整数")

if way == 0:
    a = umu.getanswerfromgithub_shen(e)
elif way == 1:
    fu = input("输入已完成该考试的用户名:")
    fp = input("输入已完成该考试的密码:")
    q = umu.getquestionlist(u,J,e)
    a = umu.getanswer(fu,fp,e,q)
else:
    exit("获取答案时发生了未知错误")

print("正在重新开始考试")
umu.retakeexam(u,J,e)
print("正在获取考试提交号")
e,ex = umu.getexamid(quiz)
print("正在开始考试")
st = umu.startexam(u,J,e,s,ex)
print("正在提交答案")
umu.saveanswer(u,J,e,a,s,ex)
print("正在结束考试")
umu.endexam(u,J,e,s,ex)
print("已完成考试")
exit(0)