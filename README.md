# 🎓 CSUAutoselect

> 中南大学自动选课工具 V2.0

原作者：[@DavidHuang](https://github.com/CrazyDaveHDY)

## ✨ 主要特性

- 🔐 支持二维码验证码输入
- 📚 支持同时进行多个课程的抢课
- 🚀 高效的选课成功率
- 🔒 本地存储，保护账户安全

## 📦 安装

### 🐍 Python3
该项目需要 Python3，可以从 [Python 官网](https://www.python.org/) 下载并安装，可以参考CSDN上[小白安装教程](https://blog.csdn.net/qq_45502336/article/details/109531599)

### 📥 下载项目
点击右上角的 `Clone or download` 下载该项目至本地

对于 git 命令行：
```console
git clone https://github.com/Ruinwalker7/CSUAutoSelect.git
```

### 📚 依赖安装

软件运行需要python包requests，在命令行中使用pip安装运行：

```console
pip3 install requests
```

## 🚀 运行

### ⚙️ 配置设置
首先修改`config.ini`，根据config中内容修改账号密码，以及填写要抢课的ID，config文件中已经详细展示了如何进行修改，**请仔细阅读**。稍后具体会展示如何找到课程的ID

### 🎯 启动程序
按照提示输入学号，教务系统密码，课程 ID 后，进入项目根目录，命令行中运行
```console
python3 autoselect.py
```

### 🔍 验证码处理
会在根目录(autoselect.py所在文件夹)生成`code.jpg`，请**人工识别二维码内容**，并输入

### ⏰ 等待选课
之后会自动检测是否开始选课，如果选课还没有开始，将会是下图的输出：

<img src="./assets/image-20230711014740394.png" alt="image-20230711014740394" style="zoom: 67%;" />

## 🔍 如何找到6位课程ID

### 📋 方法一：按教师查询
课程 ID 查找方法：在 [中南大学教务系统课表查询页面](http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_find_jg0101.jsp?xnxq01id=2022-2023-2&init=1&isview=0) 中点击「按教师」按钮，输入学年学期、教师名称后点击「查询」，格子中央的 6 位数字编号即为课程 ID，这样可以找到公选和体育的ID

   ![课程 ID.png](https://i.loli.net/2021/01/13/G7mN9BUzpaHRtkw.png)

### 📅 方法二：按时间查询
在查询页面按照时间查询，里面课表都有开课编号

<img src="./assets/image-20230711015054530.png" alt="image-20230711015054530" style="zoom:80%;" />


## ⚠️ 声明

因为每学期选课的情况可能都会发生变化，当前代码仅保证能在2025年7月之前使用，仅能提供较高的成功率，但不保证所有课程均能抢课成功；

该程序仅保存账户密码在本地，不会危害到你的账户安全；

**脚本所使用的方法并不会对服务器造成太多的负担**，能够有效避免因为选课页面无法快速打开选课页面而导致的抢课失败。

## 📋 版本说明

### 🔥 当前版本 (HEAD)
- 最新功能版本，包含登录检测功能
- 能够正确提示登录失败和验证码错误
- 建议在测试通过后使用

### 🛡️ 稳定版本 (fca3c19)
- 经过测试的稳定版本
- 功能完整，但存在验证码和登录信息错误时无提示的问题
- 如需切换到此版本，请执行以下命令：

```bash
# 切换到稳定版本
git checkout fca3c19

# 如需返回最新版本
git checkout master
```

### 📝 测试反馈
如果你测试通过了某个版本，请通过以下方式告知：
- 在GitHub Issues中反馈测试结果
- 说明测试的版本号和测试环境
- 描述遇到的问题或改进建议

## 📄 许可协议

CSUAutoSelect [GPL-3.0 License](https://github.com/CrazyDaveHDY/CSUAutoSelect/blob/master/LICENSE)

