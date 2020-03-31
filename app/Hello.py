# -*- coding:utf-8 -*-
import html
from base64 import b64encode
import os
import pymysql
import json
import telegram
import configparser
import logging
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_parameter, get_page_args
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler,Dispatcher,Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import InlineQueryHandler
from telegram.ext.dispatcher import run_async
from functools import wraps
import os
import random
import time
import re
from flask_sqlalchemy import SQLAlchemy
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from app.db_mysql import Xjj,db
from app.controller import XjjDao

def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        return
    except BadRequest:
        # handle malformed requests - read more below!
        return
    except TimedOut:
        # handle slow connection problems
        return
    except NetworkError:
        # handle other connection problems
        return
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        return
    except TelegramError:
        # handle all other telegram related errors
        return


#从配置文件读取TELEGRAM BOT的TOKEN值
proDir = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(proDir, "config.ini")
#欢迎消息列表
welcome_dir = os.path.join(proDir, "message/")
message_list = os.listdir(welcome_dir)
logs_dir= os.path.join(proDir, "logs")
path = os.path.abspath(configPath)
config = configparser.ConfigParser()
config.read(path, encoding="utf-8")
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
# Initial Flask app
app = Flask(__name__)
#数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLAlchemy']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['SQLAlchemy']['SQLALCHEMY_TRACK_MODIFICATIONS']

#print(config.sections())
updater = Updater(config['TELEGRAM']['ACCESS_TOKEN'], use_context=True, workers=32)


#写一个包函数
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


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
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

#@run_async
@send_typing_action
def getXjjInfo(update,context):
    """Send a message when the command /xingxi is issued."""
    if len(context.args)!=2:
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的查询命令 例如:/xjj 兼职 北京')
        return
    style= ''.join(context.args[0])
    district=''.join(context.args[1])
    if style not in ("兼职","洗浴","外围","酒店","丝足"):
        context.bot.send_message(chat_id=update.effective_chat.id, text='请输入正确的类别 例如:/xjj 兼职 北京')
        return
    print(district,style)
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306,user='root', passwd='123qwe', db='gatherinfo', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sqlSel = "select * from detail_info where   LOCATE('{0}', style)>0  and locate('{1}',district)>0  ORDER BY RAND()  limit 1".format(style,district)
    fast_sql = "select * from detail_info q1 inner join (select (min(q2.id) + round(rand()*(max(q2.id) - min(q2.id)))) as id from detail_info q2 where  LOCATE('{0}', q2.style)>0  and locate('{1}',q2.district)>0) as t on q1.id >= t.id limit 1".format(style,district)
    print(sqlSel)
    # 使用 execute()  方法执行 SQL 查询
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        xiaojj = {}
        data = {}
        if rs==None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="你查询的地方没有小姐姐性息，或者查询失败",
                                     parse_mode=telegram.ParseMode.HTML)
        else:
            #print("Database version : %s " % rs[1])
            xiaojj['id'] = rs[0]
            xiaojj['title']=rs[3]
            xiaojj['district']=rs[5]
            xiaojj['detailAddr']=rs[6]
            xiaojj['age']=rs[9]
            xiaojj['appear']=rs[11]
            xiaojj['price']=rs[13]
            xiaojj['serive']=rs[12]
            xiaojj['contact']="https://www.younglass.com/image/{0}".format(xiaojj['id'])
            contact = "<a href ='{0}'>点击查看，耐心等待</a>".format(xiaojj['contact'])
            xiaojj['detail']=rs[19]
            xiaojj['detail'] = re.sub("<[^>]*?>", "", xiaojj['detail'])
            xiaojj['detail'] = html.unescape(xiaojj['detail'])

            out_put1 = "主题:{0}\n区域:{1}\n地址:{2}\n价位:{3}\n编号:{4}\n服务:{5}\n详情:{6}\n联系:{7}\n"\
                .format(xiaojj['title'], xiaojj['district'],xiaojj['detailAddr'], xiaojj['price'],xiaojj['id'],\
                        xiaojj['serive'],xiaojj['detail'],contact)
            context.bot.send_message(chat_id=update.effective_chat.id, text=out_put1,
                 parse_mode=telegram.ParseMode.HTML)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

#欢迎新加入群组的人
def welcome(update, context):
    for new_user_obj in update.message.new_chat_members:
        open(logs_dir+"/logs_" + time.strftime('%d_%m_%Y') + ".txt","w").write("\nupdate status: " + str(update))
        chat_id = update.message.chat.id
        new_user = ""
        message_rnd = random.choice(message_list)
        WELCOME_MESSAGE = open(welcome_dir + message_rnd , 'r', encoding='UTF-8').read().replace("\n", "")

        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];
        WELCOME_MESSAGE=WELCOME_MESSAGE.replace("username",str(new_user))
        print(WELCOME_MESSAGE)
        context.bot.send_message(chat_id=chat_id, text=WELCOME_MESSAGE, parse_mode=telegram.ParseMode.HTML)

# 注册一个任务分派器
dispatcher = updater.dispatcher
# 将回调函数绑定到分派器上
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dispatcher.add_handler(CommandHandler("xjj", getXjjInfo))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_error_handler(error_callback)

with app.app_context(): # 添加这一句，否则会报数据库找不到application和context错误
    db.init_app(app) # 初始化db
    users = Xjj.query.filter(Xjj.id.in_(list(range(1, 101))))
def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = users.count()
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('student.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/image/<id>')
def getXjjContact(id):
    #通过id查询数据库
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306,user='root', passwd='123qwe', db='gatherinfo', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sqlSel = "select contact from detail_info where id={0}".format(id)
    # 使用 execute()  方法执行 SQL 查询
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        xiaojjzhaopian=b64encode(rs[0]).decode("utf-8")
        print(xiaojjzhaopian)
    except Exception as e:
        xiaojjzhaopian = ''
        print(e)
    finally:
        #把小姐姐照片显示出来
        return render_template('xiaojjzhaopian.html',xiaojjzhaopian=xiaojjzhaopian)
        # 关闭数据库连接
        # 关闭游标
        cursor.close()
        db.close()




if __name__ == '__main__':
    pemPath = os.path.join(proDir, "3660880_www.younglass.com.pem")
    print(pemPath)
    keyPath = os.path.join(proDir, "3660880_www.younglass.com.key")
    print(keyPath)
    app.run(debug = True, ssl_context=(pemPath, keyPath))