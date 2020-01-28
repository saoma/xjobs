# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.1
# update_date：2020-01-28

# 自己封装的SMTP发送邮件类，一般用于QQ邮箱SMTP发信

import smtplib
import email.utils
from email.message import EmailMessage
import os

try:
	# 外部使用本包导入方式
	from .xs_sendmail_setting import sender, receiver, username, password
except:
	# 测试本python代码用的导入方式
	from xs_sendmail_setting import sender, receiver, username, password

def sendmail(sender = sender,
			 receiver = receiver,
			 username = username,
			 password = password,
			 subject = 'Python3发送邮件测试',
			 content_text = '这是一封测试邮件，收到该邮件表示服务器可以正常发送邮件',
			 cc_receiver = '',
			 bcc_receiver = '',
			 content_type = 'plain',
			 host = 'smtp.qq.com',
			 port = 465,
			 img_list = [],
			 attach_list = [],
			 debug = 0):

	'''
	发送邮件功能帮助：
	
	==============================
	入参：

	sender 发件人，string，只能填写一个，如'xxx<xxx@xxx.com>'，可添加昵称也可以不加，注意邮箱必须要和鉴权登录账号相同

	receiver 收件人，string，可填写多个，用英文半角逗号,分隔，如'xxx<xxx@xxx.com>,xxx@xxx.com'，可添加昵称也可以不加

	username 登录用户名，string

	password 登录密码，string

	subject 主题，string，默认为'Python3发送邮件测试'

	content_text 邮件正文，string，可以是普通内容或HTML格式内容，默认为'这是一封测试邮件，收到该邮件表示服务器可以正常发送邮件'

	cc_receiver 抄送人，string，可填写多个，用英文半角逗号,分隔，如'xxx<xxx@xxx.com>,xxx@xxx.com'，
	可添加昵称也可以不加，默认为''

	bcc_receiver 密送人，可以接收到邮件但不会展示在接收人列表中，string，可填写多个，用英文半角逗号,分隔，
	如'xxx<xxx@xxx.com>,xxx@xxx.com'，可添加昵称也可以不加，默认为''
	
	content_type 邮件正文类型，string，普通内容填写'plain'，HTML内容填写'html'，默认为'plain'

	host SMTP服务器主机，string，默认为'smtp.qq.com'

	port 端口，int，默认为465

	img_list 图片列表（正文中引用），list，列表的元素为dict，字典键值：'imgpath' 图片地址，相对或绝对路径，
	Windows下的路径应用两个\表示；'imgID' 图片ID，在HTML正文中引用，可自动生成。
	若正文中不引用该图片，是希望作为附件的，可放到attach_list参数中传入
	默认为[]
	如：
	import email.utils
	image_id = email.utils.make_msgid()
	# 太长可能有问题，只取其中的部分即可
	image_id = image_id[1:13]
	content_text = '<img src="cid:' + image_id + '" />'
	content_type = 'html'
	img_list = [{"imgpath": "邮件发送\\图片\\star.jpg", "imgID": image_id}]

	attach_list 附件列表，list，列表元素为string，为附件地址，相对或绝对路径。Windows下的路径应用两个\表示
	默认为[]
	如：
	attach_list = ["邮件发送\\附件\\附件一张.jpg", "邮件发送\\附件\\小人走路.gif"]

	debug 调试模式，当该值非0时会显示一些调试信息，默认为0
	
	==============================
	其他注意事项：
	
	1.该函数不传入任何参数也可以进行测试
	2.本文件可以直接运行，进行测试
	'''

	# 创建邮件对象
	msg = EmailMessage()
	# 设置邮件正文内容
	msg.set_content(content_text, content_type, 'utf-8')
	# 设置主题
	msg['Subject'] = subject
	# 设置发件人
	msg['From'] = sender
	# 设置收件人，如果有多个的，传入的字符串多个之间使用,分隔，程序会自动处理，支持“昵称<邮箱地址>”的形式
	msg['To'] = receiver.split(",")
	receiverlist = receiver
	# 设置抄送人，如果有多个的，传入的字符串多个之间使用,分隔，程序会自动处理，支持“昵称<邮箱地址>”的形式
	if cc_receiver != '':
		msg['Cc'] = cc_receiver.split(",")
		receiverlist = receiverlist + "," + cc_receiver
	# 设置密送人，如果有多个的，传入的字符串多个之间使用,分隔，程序会自动处理，支持“昵称<邮箱地址>”的形式
	if bcc_receiver != '':
		receiverlist = receiverlist + "," + bcc_receiver
	# 设置加载的图片
	for imginfo in img_list:
		if imginfo.get("imgpath") and imginfo.get("imgID"):
			if os.path.exists(imginfo["imgpath"]):
				with open(imginfo["imgpath"], 'rb') as f:
					msg.add_attachment(f.read(),
									   maintype = 'image',
									   subtype = os.path.splitext(imginfo["imgpath"])[1].replace(".", ""),
									   filename = os.path.split(imginfo["imgpath"])[1],
									   cid = imginfo["imgID"])
	# 加载附件：
	for attach_file in attach_list:
		if os.path.exists(attach_file):
			with open(attach_file, 'rb') as f:
				# 不在正文中引用图片啥的，是附件，不用指定cid
				msg.add_attachment(f.read(),
								   maintype = 'application',
								   subtype = os.path.splitext(attach_file)[1].replace(".", ""),
								   filename = os.path.split(attach_file)[1])

	# 正式发送
	try:
		# 创建SMTP连接，一定要使用SSL连接！
		conn = smtplib.SMTP_SSL(host, port = port)
		# 设置调试级别，0为不输出调试信息，1为输出调试信息
		if debug != 0:
			conn.set_debuglevel(1)
		# 登录服务器
		conn.login(username, password)
		# 发送邮件
		conn.sendmail(sender, receiverlist.split(","), msg.as_string())
		# 退出连接
		conn.quit()
		if debug != 0:
			print("\n原始邮件内容为：\n" + msg.as_string())
		return True
	except Exception as e:
		print('发送邮件报错，%s' % (str(e)))

		return False

# 快速将传入的内容头尾加上<p>标签
def text_html(text):
	'''
	快速将传入的内容头尾加上<p>标签
	'''
	return "<p>%s</p>" % text

if __name__ == '__main__':
	# 发送邮件测试
	sender = sender
	receiver = receiver
	subject = '测试邮件主题'

	# 普通文本正文测试
	# content_text = '看到我表示测试成功！'
	# 普通文本正文测试

	# 快速生成html文本测试
	# content_text = '看到我表示测试成功！\n这是第二行内容\n这是第三行'
	# final_content_text = ''
	# for i in content_text.split("\n"):
	# 	print(i, text_html(i))
	# 	final_content_text = final_content_text + text_html(i)
	# print(final_content_text)
	# content_text = final_content_text
	# content_type = 'html'
	# 快速生成html文本测试

	# 正文带图片测试
	# image_id = email.utils.make_msgid()
	# # 太长可能有问题，只取其中的部分即可
	# image_id = image_id[1:13]
	# # print(image_id)
	# content_text = '看到我表示测试成功！\n如下是一张图片：\n<img src="cid:' + image_id + '" />'
	# final_content_text = ''
	# for i in content_text.split("\n"):
	# 	# print(i, text_html(i))
	# 	final_content_text = final_content_text + text_html(i)
	# # print(final_content_text)
	# content_text = final_content_text
	# content_type = 'html'
	# img_list = [{"imgpath": "邮件发送\\图片\\star.jpg", "imgID": image_id}]
	# 正文带图片测试

	# 正文带图片和附件测试
	image_id = email.utils.make_msgid()
	# 太长可能有问题，只取其中的部分即可
	image_id = image_id[1:13]
	# print(image_id)
	content_text = '看到我表示测试成功！\n如下是一张图片：\n<img src="cid:' + image_id + '" />'
	final_content_text = ''
	for i in content_text.split("\n"):
		print(i, text_html(i))
		final_content_text = final_content_text + text_html(i)
	print(final_content_text)
	content_text = final_content_text
	content_type = 'html'
	img_list = [{"imgpath": "邮件发送\\图片\\star.jpg", "imgID": image_id}]
	attach_list = ["邮件发送\\附件\\附件一张.jpg", "邮件发送\\附件\\小人走路.gif"]
	# 正文带图片和附件测试

	cc_receiver = ''
	bcc_receiver = ''

	res = sendmail(sender = sender,
				   receiver = receiver,
				   subject = subject,
				   content_text = content_text,
				   debug = 1,
				   cc_receiver = cc_receiver,
				   bcc_receiver = bcc_receiver,
				   content_type = content_type,
				   img_list = img_list,
				   attach_list = attach_list)
	if res:
		print("发送邮件成功！")
	else:
		print("发送邮件失败！")