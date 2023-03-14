import umu

u = input("输入用户名:")
p = input("输入密码:")
s,u,J = umu.login(u,p)

quiz = input("输入考试号:")
e,ex = umu.getexamid(u,J,quiz)

while True:
    try:
        way = int(input("使用GitHub上的OldGodShen/umu-json答案库(0),使用已完成账号获取答案(1):"))
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
    a = umu.getanswer(u,p,e,q)
else:
    exit("获取答案时发生了未知错误")

umu.retakeexam(u,J,e)
e,ex = umu.getexamid(u,J,quiz)
st = umu.startexam(u,J,e,s,ex)
umu.saveanswer(u,J,e,a,s,ex)
umu.endexam(u,J,e,s,ex)