#!/bin/env python
# -*- coding: utf-8 -*- 
import web, sys
import hashlib, urllib, urllib2, re, time, json
import xml.etree.ElementTree as ET
import dba,myconf,unittest

Keyword = {'apply':'bm','friend':'py','register':'zc','unregister':'zx','create_game':'cj','showgame':'hd','quitgame':'qx','game':'yx'}

reload(sys)
sys.setdefaultencoding('utf8')


def handleAuthentication(data):
    echostr = data.echostr
    if verification(data) and echostr is not None:
        return data.echostr
    return 'access verification fail'


def handlePostMessage(data):
    if verification(data):
        raw = web.data()
        msg = passContent(raw)
        if user_subscribe_event(msg):
            return help_info(msg)
        elif is_text_msg(msg):
            return handleContent(msg)
    return 'message processing fail'


def verification(data):
    signature = data.signature
    timestamp = data.timestamp
    nonce = data.nonce
    token = myconf.WEIXIN_TOKEN
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    print hashstr
    if hashstr == signature:
        return True
    return False


def passContent(content):
    root = ET.fromstring(content)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

HELP_INFO = \
u"""
潮白风云队秘欢迎你！
快试试一下几条指令吧：
1. hd : 最新活动预告
2. zc+空格+昵称 : 注册成为潮白风云队员
3. bm :  已注册球员，直接发送本指令报名最新一期活动
4. py+空格+朋友姓名 ： 帮朋友报名活动
5. qx : 取消报名(损人品[偷笑])
6. yx : 足球游戏(未开通)
7. zx : 注销球员身份(不推荐，除非想更改昵称信息)
8. 重看本指令请回复help或问号
"""


def help_info(msg):
    return response_text_msg(msg, HELP_INFO)


TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""


def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content)
    return s


def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'


def is_text_msg(msg):
    return msg['MsgType'] == 'text'


def handleContent(msg):
    content = msg['Content']
    if content == '?' or content == u'？' or content == 'help' or content == u'帮助':
        return help_info(msg)
    else:
        return handleRule(msg)


def handleRule(msg):
    key = msg['Content'][0:2].lower()
    content = msg['Content'][3:]
    if key == Keyword['apply']:
        name = u'%s' % (msg['FromUserName'])
        #update the user_info with the latest game id
        user_info = dba.get_username(name)
        gameinfo = dba.get_latestgames()
        if user_info:
            #TODO: update the user_info with the new name
            if user_info.game_id == gameinfo.id:
                return response_news_msg(msg, u"""山炮啊，你已经报名过了！""")
            else:
                dba.update_usergame(name, str(user_info.name), gameinfo.id)
                info = u'给力啊！报名成功\n以下是活动信息:\n%s' % (show_latestgame())
                return response_news_msg(msg, info)
        else:
            return response_news_msg(msg, u"""哥，别着急，先注册一下球员信息呗～\n发送zc+空格+英文昵称 : 注册成为队员""")
    if key == Keyword['friend']:
        if content:
            gameinfo = dba.get_latestgames()
            friend = dba.get_username(content)
            print friend
            if friend:
                dba.update_usergame(content, content, gameinfo.id)
                return response_news_msg(msg, u'谢谢帮朋友报名！')
            else:
                dba.insert_userinfo(content, content, gameinfo.id)
                return response_news_msg(msg, u'谢谢你介绍新朋友过来！')
        else:
            return response_news_msg(msg, u'你要帮谁报名？请发送 py+空格+朋友姓名！')
    elif key == Keyword['quitgame']:
        name = u'%s' % (msg['FromUserName'])
        #update the user_info with the latest game id
        user_info = dba.get_username(name)
        gameinfo = dba.get_latestgames()
        if user_info:
            #TODO: update the user_info with the new name
            if user_info.game_id == gameinfo.id:
                dba.update_usergame(name, str(user_info.name), 0)
                return response_news_msg(msg, u"""您已经取消报名！人品－1""")
            else:
                return response_news_msg(msg, u"""你还没有报名，怎么取消？""")
        else:
            return response_news_msg(msg, u"""你没注册，当然也不能取消报名了，请先注册然后完成报名""")
    elif key == Keyword['create_game']:
        #split location ,date and time
        array = content.split(' ')
        if len(array) < 3:
                return help_info(msg)
        #id accurate limit to second is enought
#        location = u'%s' % array[0]
        dba.insert_game(int(time.time()), array[0], array[1], array[2])
        return response_news_msg(msg, u"""活动创建成功！""")
    elif key == Keyword['showgame']:
        name = u'%s' % (msg['FromUserName'])
        user_info = dba.get_username(name)
        if user_info:
            return response_news_msg(msg, show_latestgame())
        else:
            return response_news_msg(msg, u'你还没注册，不能查看最新活动~请发送zc+空格+姓名 注册为潮白风云队员')
    elif key == Keyword['register']:
        name = u'%s' % (msg['FromUserName'])
        #update the user_info with the latest game id
        user_info = dba.get_username(name)
        if user_info:
            return response_news_msg(msg, u"你已经是在册球员，请不要重复注册")
        if content:
            dba.insert_userinfo(msg['FromUserName'], content, 0)
        else:
            return response_news_msg(msg, u"昵称不能为空，请输入：zc＋空格＋英文昵称")
        return response_news_msg(msg, u"""注册成功！""")
    elif key == Keyword['unregister']:
        dba.del_user_info(msg['FromUserName'])
        return response_news_msg(msg, u"""注销成功！""")
    elif key == Keyword['game']:
        return response_news_msg(msg, u"""游戏功能尚未开通，请多提反馈意见!\n发送fk＋空格＋内容:本助理洗耳恭听""")
    else:
        return response_news_msg(msg, u"""无聊？回复'?' 获取帮助""")


def show_latestgame():
    gameinfo = dba.get_latestgames()
    if gameinfo:
        info = u"""地点: %s \n日期: %s \n时间: %s \n参与球星: %s""" % (gameinfo.location, str(gameinfo.date), str(gameinfo.time), str(dba.get_usersbygameid(gameinfo.id)))
        return info
    else:
        info = u"""目前没有比赛被创建～"""
        return info


def response_news_msg(recvmsg, info):
    msgHeader = TEXT_MSG_TPL % (recvmsg['FromUserName'], recvmsg['ToUserName'], str(int(time.time())), info)

    return msgHeader
