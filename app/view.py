import configparser
import html
import logging
import os
import re
import time
from base64 import b64encode
from functools import wraps
from random import random, choice
import pymysql
import telegram
from flask import request, render_template, Blueprint, flash, redirect, url_for, jsonify, json
from flask_paginate import Pagination, get_page_parameter, get_page_args
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from app.controller import XjjDao


# 定义蓝图
xiaojiejie = Blueprint('xiaojiejie', __name__, template_folder='templates')


def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


# 查询 城市 类别 的十个 小姐姐性息 分页显示
@xiaojiejie.route('/jsondata', methods=['POST', 'GET'])
def infos():
    """
     查询 城市 类别 的十个 小姐姐性息 分页显示
    """
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        info = request.values
        print(info)
        limit = int(info.get('limit', 10))  # 每页显示的条数
        offset = int(info.get('offset', 0))  # 分片数，(页码-1)*limit，它表示一段数据的起点
        district = info.get('district')  # 获取地方，默认北京
        style = info.get('style')  # 获取 性息类型
        print('get', limit)
        print('get  offset', int(offset / limit) + 1)
        print('get  district', district)
        print('get  style', style)
        xjjservice = XjjDao()
        paginate = xjjservice.list_page_bootstrap(district, style, offset, limit)
        # 获取最新的每个城市的前100条数据
        data = []
        for i in paginate:
            i.contact = url_for('xiaojiejie.getXjjContact', id=i.id)
            a = serialize(i)
            print(a)
            data.append(a)
        return jsonify({'total': paginate.total, 'rows': data})
        # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
        # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了


# 查询telegram里面分享的最新节点信息
@xiaojiejie.route('/updatelist', methods=['GET', 'POST'])
def updatelist():
    return render_template('updatelist.html')

@xiaojiejie.route('/update',methods = ['POST', 'GET'])
def update():
   if request.method == 'POST':
      v2rayn = {}
      time = request.form['time']
      text = request.form['text']
      #插入数据库
      # 打开数据库连接
      db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123qwe', db='gatherinfo', charset='utf8')
      # 使用 cursor() 方法创建一个游标对象 cursor
      try:
          cursor = db.cursor()
          cursor.execute("TRUNCATE TABLE `v2rayn`;")
          cursor.execute("INSERT INTO `v2rayn` (`time`, `text`) VALUES ('{0}', '{1}');".format(time,text))
      except:
          db.rollback()
          db.close()
          raise
      else:
          db.commit()
          db.close()
      return redirect(url_for('xiaojiejie.nodelist',v2rayn = v2rayn))

# 查询telegram里面分享的最新节点信息
@xiaojiejie.route('/nodelist', methods=['GET', 'POST'])
def nodelist():
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306,user='root', passwd='123qwe', db='gatherinfo', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sqlSel = "select * from v2rayn limit 1"

    print(sqlSel)
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        v2rayn = {}
        v2rayn['time'] = rs[0]
        v2rayn['text']=rs[1]
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
    return render_template('nodelist.html',v2rayn=v2rayn)


# 小姐姐性息分页查询
@xiaojiejie.route('/pagination1', methods=['GET', 'POST'])
def pagination1():
    return render_template('pagination1.html')


# GHB展示界面
@xiaojiejie.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')


@xiaojiejie.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@xiaojiejie.route('/citys', methods=['GET', 'POST'])
def get_citys():
    xjjservice = XjjDao()
    citys = xjjservice.get_xjj_citys()
    # 获取最新的每个城市的前100条数据
    data = []
    for i in citys:
        if i[0] is not None:
            data.append(i[0])
    print(data)
    a = jsonify({'citys': data})
    return a


@xiaojiejie.route('/details19880424', methods=['POST', 'GET'])
def get_xjj_detial():
    # 如果是post就返回json数据
    if request.method == 'POST':
        print('post')
        id = int(request.form.get("id"))
        xjjservice = XjjDao()
        # return book list to front end
        xjj_details = xjjservice.get_details_by_id(id)
        # 把联系方式blob转成Utf8
        xjj_details.contact = b64encode(xjj_details.contact).decode("utf-8")
        # 去除标签
        xjj_details.detail = re.sub("<[^>]*?>", "", xjj_details.detail)
        xjj_details.detail = html.unescape(xjj_details.detail)
        data = serialize(xjj_details)
        # print(a)
        return jsonify({'data': data})
    if request.method == 'GET':
        info = request.values
        id = int(info.get('id', 1))
        xjjservice = XjjDao()
        # return book list to front end
        xjj_details = xjjservice.get_details_by_id(id)
        if xjj_details == None:
            return render_template('error_page.html')

        # 把联系方式blob转成Utf8
        xjj_details.contact = b64encode(xjj_details.contact).decode("utf-8")
        # 去除标签
        xjj_details.detail = re.sub("<[^>]*?>", "", xjj_details.detail)
        xjj_details.detail = html.unescape(xjj_details.detail)
        a = serialize(xjj_details)
        # print(a)
        return render_template('details.html', xjj=a)


@xiaojiejie.route('/pagination', methods=['GET', 'POST'])
def xjj_page():
    # 获取页面传过来的页数
    page = int(request.args.get('page', 1))  # 如没获取到 默认给个第一页
    # 给每页分多少条数据   这里是每页显示10条
    per_page = int(request.args.get('per_page', 10))
    # 分页需要的2参数 第一个是当前页 第二个是每页显示多少条
    xjjservice = XjjDao()
    # return book list to front end
    paginate = xjjservice.list_page_district("北京", page, per_page)
    # 获取最新的每个城市的前100条数据
    paginate.total = 100
    stus = paginate.items
    return render_template('pagination.html', pagination=paginate, users=stus)


@xiaojiejie.route('/image/<id>')
def getXjjContact(id):
    xjjservice = XjjDao()
    notes = b64encode(xjjservice.get_contact_by_id(id)).decode("utf-8")
    print(notes)
    return render_template('xiaojjzhaopian.html', xiaojjzhaopian=notes)


# 从配置文件读取TELEGRAM BOT的TOKEN值
proDir = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(proDir, "config.ini")
# 欢迎消息列表
welcome_dir = os.path.join(proDir, "message/")
message_list = os.listdir(welcome_dir)
logs_dir = os.path.join(proDir, "logs")
path = os.path.abspath(configPath)
config = configparser.ConfigParser()
config.read(path, encoding="utf-8")
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
# print(config.sections())
updater = Updater(config['TELEGRAM']['ACCESS_TOKEN'], use_context=True, workers=32)


# updater.bot.setWebhook('https://bot.khashtamov.com/planet/bot/{bot_token}/'.format(bot_token=bot_token))

# 写一个包函数
def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(telegram.ChatAction.TYPING)
send_upload_video_action = send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(telegram.ChatAction.UPLOAD_PHOTO)


# webhook for telegram
@xiaojiejie.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    """https://api.telegram.org/bot1080551756:AAFyFgZ3jBg6F4bIFk5IK9Wko8X59eTPSpU/setwebhook?url=https://www.younglass.com/hook"""
    if request.method == "POST":
        print(request.get_json(force=True))
        update = telegram.Update.de_json(request.get_json(force=True), updater.bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


@send_typing_action
def reply_handler(update, context):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)


@send_typing_action
def start(update, context):
    '''这是一个全国小姐姐性息查询机器人，每天更新全国各地小姐姐性息。
    请输入 /xingxi <地名> 开始你的表演！每次随机选取一个地区的小姐姐联系方式发出来'''
    update.message.reply_text("这是一个全国小姐姐性息查询机器人，每天更新全国各地小姐姐性息。\n\
    输入:/xjj <兼职> <城市名> 查询当前城市兼职妹子性息\n\
    输入:/xjj <洗浴> <城市名> 查询当前城市洗浴中心性息\n\
    输入:/xjj <外围> <城市名> 查询当前城市外围女性息\n\
    输入:/xjj <酒店> <城市名> 查询当前城市酒店妹子性息\n\
    输入:/xjj <丝足> <城市名> 查询当前城市丝足会所性息\n\
    每次随机选取一个地区的小姐姐联系方式发出来")


@send_typing_action
def get_rand_xjj(update, context):
    """Send a message when the command /xjj is issued."""
    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的查询命令 例如:/xjj 兼职 北京')
        return
    style = ''.join(context.args[0])
    district = ''.join(context.args[1])
    if style not in ("兼职", "洗浴", "外围", "酒店", "丝足"):
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的类别 例如:/xjj 兼职 北京')
        return
    print(district, style)
    xjjservice = XjjDao()
    rs = xjjservice.get_rand_xjj_for_tg(style, district)
    if rs == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="你查询的地方没有小姐姐性息，或者查询失败",
                                 parse_mode=telegram.ParseMode.HTML)
    else:
        # 把联系方式做成超链接
        contact = "http://www.younglass.com/image/{0}".format(rs.id)
        contact = "<a href ='{0}'>点击查看，耐心等待</a>".format(contact)
        # 处理Detail数据 过滤掉telegram send message 中 不允许的Html标签和字符
        rs.detail = re.sub("<[^>]*?>", "", rs.detail)
        rs.detail = html.unescape(rs.detail)
        out_put1 = "主题:{0}\n区域:{1}\n地址:{2}\n价位:{3}\n编号:{4}\n服务:{5}\n详情:{6}\n联系:{7}\n" \
            .format(rs.title, rs.district, rs.detailAddr, rs.price, rs.id, rs.service, rs.detail, contact)
        context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
                                 parse_mode=telegram.ParseMode.HTML)


# 欢迎新加入群组的人
def welcome(update, context):
    for new_user_obj in update.message.new_chat_members:
        open(logs_dir + "/logs_" + time.strftime('%d_%m_%Y') + ".txt", "w").write("\nupdate status: " + str(update))
        chat_id = update.message.chat.id
        new_user = ""
        message_rnd = random.choice(message_list)
        WELCOME_MESSAGE = open(welcome_dir + message_rnd, 'r', encoding='UTF-8').read().replace("\n", "")

        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];
        WELCOME_MESSAGE = WELCOME_MESSAGE.replace("username", str(new_user))
        print(WELCOME_MESSAGE)
        context.bot.send_message(chat_id=chat_id, text=WELCOME_MESSAGE, parse_mode=telegram.ParseMode.HTML)


# 注册一个任务分派器
dispatcher = updater.dispatcher
# 将回调函数绑定到分派器上
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dispatcher.add_handler(CommandHandler("xjj", get_rand_xjj))
dispatcher.add_handler(CommandHandler("start", start))


# @run_async
@send_typing_action
def getXjjInfo(update, context):
    """Send a message when the command /xingxi is issued."""
    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的查询命令 例如:/xjj 兼职 北京')
        return
    style = ''.join(context.args[0])
    district = ''.join(context.args[1])
    if style not in ("兼职", "洗浴", "外围", "酒店", "丝足"):
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的类别 例如:/xjj 兼职 北京')
        return
    print(district, style)
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123qwe', db='gatherinfo', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sqlSel = "select * from detail_info where   LOCATE('{0}', style)>0  and locate('{1}',district)>0  ORDER BY RAND()  limit 1".format(
        style, district)
    fast_sql = "select * from detail_info q1 inner join (select (min(q2.id) + round(rand()*(max(q2.id) - min(q2.id)))) as id from detail_info q2 where  LOCATE('{0}', q2.style)>0  and locate('{1}',q2.district)>0) as t on q1.id >= t.id limit 1".format(
        style, district)
    print(sqlSel)
    # 使用 execute()  方法执行 SQL 查询
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        xiaojj = {}
        data = {}
        if rs == None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="你查询的地方没有小姐姐性息，或者查询失败",
                                     parse_mode=telegram.ParseMode.HTML)
        else:
            # print("Database version : %s " % rs[1])
            xiaojj['id'] = rs[0]
            xiaojj['title'] = rs[3]
            xiaojj['district'] = rs[5]
            xiaojj['detailAddr'] = rs[6]
            xiaojj['age'] = rs[9]
            xiaojj['appear'] = rs[11]
            xiaojj['price'] = rs[13]
            xiaojj['serive'] = rs[12]
            xiaojj['contact'] = "https://www.younglass.com/image/{0}".format(xiaojj['id'])
            contact = "<a href ='{0}'>点击查看，耐心等待</a>".format(xiaojj['contact'])
            xiaojj['detail'] = rs[19]
            xiaojj['detail'] = re.sub("<[^>]*?>", "", xiaojj['detail'])
            xiaojj['detail'] = html.unescape(xiaojj['detail'])

            out_put1 = "主题:{0}\n区域:{1}\n地址:{2}\n价位:{3}\n编号:{4}\n服务:{5}\n详情:{6}\n联系:{7}\n" \
                .format(xiaojj['title'], xiaojj['district'], xiaojj['detailAddr'], xiaojj['price'], xiaojj['id'], \
                        xiaojj['serive'], xiaojj['detail'], contact)
            context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
                                     parse_mode=telegram.ParseMode.HTML)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()