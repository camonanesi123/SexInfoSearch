# SexInfoSearch 一个简单的小姐姐性息查询网站
============================================
![](https://github.com/camonanesi123/SexInfoSearch/blob/master/app/static/favicon.png) 

## 使用技术 telegramBot python flask sqlAldemy ajax bootstrap json mysql

*一、环境配置
*安装数据库mysql</br>
*安装Python3</br>
'''Bash
wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz </br>
tar Jxvf Python-3.5.1.tar.xz </br>
cd Python-3.5.1  </br>
./configure --prefix=/usr/local/python3 </br>
make && make install </br>
'''

*新建指向新版本 Python 以及 pip 的软连接</br>
'''Bash
cp /usr/local/python3/bin/python3 /usr/bin/python3 </br>
ln -s /usr/local/python3/bin/python3.5 /usr/bin/python3 </br>
python3 -v 查看是否安装成功 </br>
pip3 -V 查看是否安装成功  </br>
pip3 install virtualenv </br>
'''
#在当前文件夹下构建虚拟环境
virtualenv -p /usr/local/python3/bin/python3 venv
#启动虚拟环境
source venv/bin/activate 

从GIT上获取 生产环境代码
git clone https://github.com/camonanesi123/SexInfoSearch.git

进入项目文件夹
cd SexInfoSearch
打开配置文件　config.py
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123qwe@localhost:3306/gatherinfo?charset=utf8"
把root后面的密码 改成你自己数据库的密码
使用pip install -r requirements.txt 安装依赖包


二、uWSGI服务器配置

uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议。Nginx中HttpUwsgiModule的作用是与uWSGI服务器进行交换。

WSGI是一种Web服务器网关接口。它是一个Web服务器（如nginx）与应用服务器（如uWSGI服务器）通信的一种规范。

uWSGI安装
uwsgi的官方文档说明：
http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html
在python虚拟环境里面直接使用pip就是 pip3了 
pip install uwsgi
修改配置文件
uwsgi.ini

[uwsgi]
# uswgi socket port
socket = 127.0.0.1:3031
#app file 改成你自己的项目启动名字
wsgi-file = server.py
callable = app
master = true
processes = 4
#http port http请求端口号
http = :8000
vacuum = true
die-on-term = true

检查python与uWSGI通讯
建立一个测试文件，以测试uwsgi是否正常运行。
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"] # python3
    #return ["Hello World"] # python2
运行uWSGI

uwsgi --http :8000 --wsgi-file test.py
另外开一个终端执行
wget 127.0.0.1:8000
检查flask与uWSGI通讯
运行uWSGI
uwsgi --http :8000 --wsgi-file service.py --callable app
wget 127.0.0.1:8000 测试是否工作正常

工作正常之后用配置文件启动uwsgi服务器
uwsgi --ini uwsgi.ini

三、配置NGINX服务器 将域名和IP地址端口号 映射到uWsgi服务器来
具体配置如下：
# mysite_nginx.conf
# the upstream component nginx needs to connect to
upstream flask {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:3031; # for a web port socket (we'll use this first)
}
# configuration of the server
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
弄好了重启一下NGINX

四、去域名解析网站 把域名 解析到 本IP地址80端口上来 然后可以测试一下

五、NGINX添加HTTPS配置

待定

六、每周使用 小姐姐爬虫 爬数据 然后同步到数据库上去

然后打开浏览器输入
162.211.224.9:8000
查看是否启动成功
