# 爬虫说明：

### 1、使用python3.6.2版本开发，界面使用python3.6版本对应的wxpython开发
### 2、界面可设置爬取数据的边界信息，如最高价格、最大平方等
### 3、框架还有登陆界面，目前登陆界面咩有用户名，只有密码输入框
### 4、使用pip安装时，如果速度慢，可以使用下面命令安装（该方法是使用国内源安装,例子中是安装wxpython
```
pip install wxpython -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```
### 5、使用以下命令打包程序成exe可执行程序
```
pyinstaller -i Search.ico -w -F main.py
```
