import umu

a = input("输入用户名:")
b = input("输入密码:")
c = input("输入考试号:")
d = input("输入已完成该考试的用户名:")
e = input("输入已完成该考试的密码:")

f,g,h,i,j = umu.login(a,b)

k,l = umu.getexamid(i,j,c)
m = umu.getquestionlist(i,j,k)
n,o = umu.getanswer(d,e,k,m)

p = umu.retakeexam(i,j,k)
k,l = umu.getexamid(i,j,c)
q = umu.startexam(i,j,k,f,l)
umu.saveanswer(i,j,k,o,f,l)
r = umu.endexam(i,j,k,f,l)