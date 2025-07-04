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

CONFIG_FILE = 'config.ini'

# 配置检测函数
REQUIRED_KEYS = [
    'username', 'password', 'semester_code',
    'public_course_count', 'major_course_count'
]


def validate_config(config):
    # 检查基础参数
    for key in REQUIRED_KEYS:
        if key not in config:
            print(f'配置文件缺少必要参数: {key}')
            sys.exit(1)
    # 检查课程数量和ID匹配
    try:
        public_count = int(config['public_course_count'])
        major_count = int(config['major_course_count'])
    except Exception:
        print('课程数量参数必须为整数')
        sys.exit(1)
    for i in range(1, public_count + 1):
        if f'public_course_id{i}' not in config:
            print(f'缺少公选课ID: public_course_id{i}')
            sys.exit(1)
    for i in range(1, major_count + 1):
        if f'major_course_id{i}' not in config:
            print(f'缺少专业课/体育课ID: major_course_id{i}')
            sys.exit(1)


def read_config():
    con = configparser.ConfigParser()
    con.read(CONFIG_FILE, encoding='utf-8')
    config = dict(con.items('config'))
    validate_config(config)
    return config


def login(session, username, password, qrcode):
    s1 = base64.b64encode(username.encode())
    s2 = base64.b64encode(password.encode())
    data = {'encoded': s1.decode() + '%%%' + s2.decode(), 'RANDOMCODE': qrcode}
    LOGIN_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk'
    MAIN_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/framework/xsMain.jsp'
    respond = session.post(LOGIN_URL, data)
    respond = session.get(MAIN_URL)
    return respond


def build_class_urls(config):
    semester = config['semester_code']
    public_count = int(config['public_course_count'])
    major_count = int(config['major_course_count'])
    urls = []
    for i in range(1, public_count + 1):
        cid = config[f'public_course_id{i}']
        urls.append(
            f'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id={semester}{cid}&xkzy=&trjf=')
    for i in range(1, major_count + 1):
        cid = config[f'major_course_id{i}']
        urls.append(
            f'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id={semester}{cid}&xkzy=&trjf=')
    return urls


def work(session, url):
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
        return False


def main():
    config = read_config()
    session = requests.Session()
    Img_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/verifycode.servlet'
    respond = session.get(Img_URL)
    with open('code.jpg', 'wb') as f:
        f.write(respond.content)
    LOGIN_URL = 'http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk'
    respond = session.get(LOGIN_URL)
    qrcode = input("输入验证码：")
    respond = login(session, config['username'], config['password'], qrcode)
    if respond.status_code != requests.codes.ok:
        print('学号或密码或验证码错误，请退出修改配置重启')
        sys.exit()
    else:
        print('成功登录教务系统')
    class_urls = build_class_urls(config)
    # 进入选课页面
    while True:
        respond = session.get('http://csujwc.its.csu.edu.cn/jsxsd/xsxk/xklc_list')
        key = re.findall('href="(.+?)" target="blank">进入选课', respond.text)
        if len(key) >= 1:
            break
        print('寻找选课列表中')
        time.sleep(0.5)
    respond = session.get('http://csujwc.its.csu.edu.cn' + key[0])
    print('成功进入选课页面')
    # 抢课主循环
    while True:
        class_urls = [url for url in class_urls if not work(session, url)]
        if len(class_urls) == 0:
            print('选课已完成，程序退出')
            break
        time.sleep(1)


if __name__ == '__main__':
    main()

