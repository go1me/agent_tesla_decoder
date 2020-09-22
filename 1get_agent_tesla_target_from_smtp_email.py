import poplib
from email.parser import Parser
import base64
# 输入邮件地址, 口令和POP3服务器地址:
email = "abc"
password = "abc"
pop3_server = "pop.yandex.com"

# 连接到POP3服务器:
server = poplib.POP3_SSL(pop3_server)
# 可以打开或关闭调试信息:
# server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome())
# 身份认证:
server.user(email)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似['1 82923', '2 2184', ...]
# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
ff= open("mail.txt","w")

for i in range(index,0,-1):
	print(i)
	resp, lines, octets = server.retr(i)
	# lines存储了邮件的原始文本的每一行,
	# 可以获得整个邮件的原始文本:
	for j in range(len(lines)):
		try:
			lines[j]=str(base64.b64decode(lines[j]), "utf-8") 
		except:
			lines[j]=lines[j].decode('utf-8')

	msg_content = '\r\n'.join(lines)
	ff.write(msg_content+"\r\n--------------->>>\r\n")
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()
ff.close()
