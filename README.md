# SexInfoSearch 一个简单的小姐姐性息查询网站
![](https://github.com/camonanesi123/SexInfoSearch/blob/master/app/static/favicon.png) 

## telegramBot python flask sqlAldemy ajax bootstrap json mysql

一、环境配置
安装数据库mysql</br>
安装Python3</br>
```Bash
wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz 
tar Jxvf Python-3.5.1.tar.xz
cd Python-3.5.1  
./configure --prefix=/usr/local/python3 
make && make install
#新建指向新版本 Python 以及 pip 的软连接</br>
cp /usr/local/python3/bin/python3 /usr/bin/python3 
ln -s /usr/local/python3/bin/python3.5 /usr/bin/python3 
python3 -v #查看是否安装成功 
pip3 -V #查看是否安装成功 
pip3 install virtualenv 

#在当前文件夹下构建虚拟环境
virtualenv -p /usr/local/python3/bin/python3 venv 
#启动虚拟环境 
source venv/bin/activate  

#从GIT上获取 生产环境代码 
git clone https://github.com/camonanesi123/SexInfoSearch.git 

#进入项目文件夹 
cd SexInfoSearch 
#打开配置文件
vi config.py 
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123qwe@localhost:3306/gatherinfo?charset=utf8" 
#把root后面的密码 改成你自己数据库的密码 
#使用安装依赖包 
pip install -r requirements.txt 
```

二、uWSGI服务器配置 </br>

uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。Nginx中HttpUwsgiModule的作用是与uWSGI服务器进行交换。 </br>
WSGI是一种Web服务器网关接口。它是一个Web服务器（如nginx）与应用服务器（如uWSGI服务器）通信的一种规范。 </br>

uWSGI安装 </br>
uwsgi的官方文档说明： </br>
http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html </br>
在python虚拟环境里面直接使用pip就是 pip3了  </br>
```Bash
pip install uwsgi
#修改配置文件 
vi uwsgi.ini 
#设置成你想要的格式
[uwsgi] 
socket = 127.0.0.1:3031  
wsgi-file = server.py 
callable = app 
master = true 
processes = 4 
http = :8000 
vacuum = true 
die-on-term = true

#检查python与uWSGI通讯  
#建立一个测试文件，以测试uwsgi是否正常运行。 
vi test.py 
```
```Python
def application(env, start_response):     
    start_response('200 OK', [('Content-Type','text/html')])   
    return [b"Hello World"] 
    #return ["Hello World"] 
```
运行uWSGI  
```Bash
uwsgi --http :8000 --wsgi-file test.py  
#另外开一个终端执行  
wget 127.0.0.1:8000 
#检查flask与uWSGI通讯 
#运行uWSGI 
uwsgi --http :8000 --wsgi-file service.py --callable app
wget 127.0.0.1:8000 #测试是否工作正常
#工作正常之后用配置文件启动uwsgi服务器 
uwsgi --ini uwsgi.ini 
```

三、配置NGINX服务器 将域名和IP地址端口号 映射到uWsgi服务器来 </br>
具体配置如下：
```Bash
#mysite_nginx.conf
#the upstream component nginx needs to connect to
upstream flask {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:3031; # for a web port socket (we'll use this first)
}
#configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name 162.211.224.93; # substitute your machine's IP address or FQDN
    charset     utf-8;
    # max upload size
    client_max_body_size 75M;   # adjust to taste
    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  flask;
        # the uwsgi_params file you installed
        include uwsgi_params;
    }
}
```

弄好了重启一下NGINX  </br>

四、去域名解析网站 把域名 解析到 本IP地址80端口上来 然后可以测试一下 </br>

五、NGINX添加HTTPS配置 </br>

待定

六、每周使用 小姐姐爬虫 爬数据 然后同步到数据库上去

#mysql -uroot -proot -D gatherinfo < detail_info.sql

然后打开浏览器输入
ip_address:8000
查看是否启动成功

```Bash
#今天遇到问题
#服务器上使用nginx+uwgsi 怎么也无法调用webhook
#刚刚看了一下官方的文档，可以通过机器人@CanOfWormsBot 来测试你的webhook是否设置好
#我还使用了 POSTMAN 模拟HTTPS 请求发送给 WEBHOOK 报文如下{"update_id": 137135676, "message": {"entities": [{"offset": 0, "length": 4, "type": "bot_command"}], "from": {"language_code": "zh-hans", "is_bot": "False", "id": 1017960142, "first_name": "komo", "username": "Komonado"}, "chat": {"type": "private", "id": 1017960142, "first_name": "komo", "username": "Komonado"}, "text": "/xjj 兼职 兰州", "date": 1585815927, "message_id": 272}} 
#POSTMAN 可以正常调用BOT 可是 TELEGRAM就不行 
```
