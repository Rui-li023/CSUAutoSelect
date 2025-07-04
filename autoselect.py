#!
# coding=utf-8
import re
import sys
import time
import requests
import base64
import configparser
from copy import deepcopy
from datetime import datetime

file = 'config.ini'
con = configparser.ConfigParser()
con.read(file, encoding='utf-8')

item = con.items('config')
item = dict(item)

def validate_config(config):
	# num1, num2 check
	try:
		num1_read = int(config.get('num1', 0))
		num2_read = int(config.get('num2', 0))
	except ValueError:
		print("错误：请检查 num1 或 num2")
		sys.exit(1)

	# id1 ~ idn check
	for i in range(1, num1_read + 1):
		key = f'id{i}'
		if key not in config or not config[key].strip():
			print(f"错误：请检查 {key}")
			sys.exit(1)

	# id_1 ~ id_n check
	for i in range(1, num2_read + 1):
		key = f'id_{i}'
		if key not in config or not config[key].strip():
			print(f"错误：请检查 {key}")
			sys.exit(1)


validate_config(item)

global username, password

Img_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/verifycode.servlet'
LOGIN_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk'
MAIN_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/framework/xsMain.jsp'

# REQUEST_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper' #公选
# REQUEST_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper' #体育和专业课

session = requests.Session()
respond = session.get(Img_URL)

semester = item['time']

with open('code.jpg', 'wb') as file:
	file.write(respond.content)
	file.close

respond = session.get(LOGIN_URL)
qrcode = input("输入验证码：")


def login():
	username = item['username']
	password = item['password']
	s1 = base64.b64encode(username.encode())
	s2 = base64.b64encode(password.encode())

	data = {'encoded': s1.decode() + '%%%' + s2.decode(), 'RANDOMCODE': qrcode}
	respond = session.post(LOGIN_URL, data)
	respond = session.get(MAIN_URL)
	return respond


respond = login()

if respond.status_code != requests.codes.ok:
	print('学号或密码或验证码错误，请退出修改配置重启')
	sys.exit()
else:
	print('成功登录教务系统')

num1 = int(item['num1'])
num2 = int(item['num2'])

class_url = []

for i in range(1, num1 + 1):
	id = item['id' + str(i)]
	class_url.append(
		'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper' + '?jx0404id=' + semester + id + '&xkzy=&trjf=')

for i in range(1, num2 + 1):
	id = item['id_' + str(i)]
	class_url.append(
		'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper' + '?jx0404id=' + semester + id + '&xkzy=&trjf=')

# 设置目标时间为2024年1月12日9点57分
# target_time = datetime(2024, 1, 12, 9, 58)
# while True:
# 	# 获取当前时间
# 	current_time = datetime.now()
# 	# 判断当前时间是否大于目标时间
# 	if current_time > target_time:
# 		print("当前时间大于2024年1月12日9点58分")
# 		break
# 	else:
# 		print("当前时间不大于2024年1月12日9点58分")
# 		time.sleep(5)

while True:
	respond = session.get('http://csujwc.its.csu.edu.cn/jsxsd/xsxk/xklc_list')
	key = re.findall('href="(.+?)" target="blank">进入选课', respond.text)
	if len(key) >= 1:
		break
	print('寻找选课列表中')
	time.sleep(0.5)

respond = session.get('http://csujwc.its.csu.edu.cn' + key[0])

print('成功进入选课页面')


def work(url):
	try:
		respond = session.get(url)
		if re.search('true', respond.text):
			print("成功抢课!")
			return True
		if re.search('冲突', respond.text):
			print(re.search('"选课失败：(.+)"', respond.text).group())
			print("课程冲突，已暂停该课程选课\n")
			return True
		if re.search('当前教学班已选择！', respond.text):
			print(re.search('"选课失败：(.+)"', respond.text).group())
			print("当前教学班已选择！\n")
			return True
		if re.search('null', respond.text):
			print("没有该 ID 所对应的课程\n")
			return False
		else:
			print(respond.text)
			print("\n")
		return False
	except Exception as e:
		print(f"发生错误: {e}")
		return False  # 发生任何错误时，返回False


while True:
	class_url = [url for url in class_url if not work(url)]
	if len(class_url) == 0:
		print('选课已完成，程序退出')
		break
	time.sleep(1)
