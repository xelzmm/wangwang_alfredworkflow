#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import alp
import os
import codecs

path = u'%s/Library/Containers/com.taobao.aliwangwang/Data/Library/Application Support/AliWangwang/profiles/' % os.path.expanduser("~")


def get_account():

    if(os.path.exists('config')):
        config = codecs.open('config', encoding='utf-8')
        account = config.readline()
        config.close()
        return account
    else:
        return False


def query(keyword):

    account = get_account()
    if not account:
        item = alp.Item(title=u'您还没有设置旺旺帐号', subtitle=u'请先使用\'setww\'命令设置旺旺帐号', valid=False)
        alp.feedback([item])
        return
    db = path + account + '/db/contact.db'
    if not os.path.exists(db):
        item = alp.Item(title=u'查询失败', subtitle=u'好友列表不存在或已加密，您可以尝试setww重新选择其他帐号', valid=False)
        alp.feedback([item])
        return
    items = []
    conn = sqlite3.connect(db)
    c = conn.cursor()
    keyword = '%%%s%%' % keyword.strip()
    try:
        c.execute('''SELECT OID,* FROM contact WHERE nickname_pinyin LIKE ? LIMIT 10''', (keyword, ))
        result = c.fetchall()
    except:
        result = []
        item = alp.Item(title=u'暂不支持中文查询，请使用拼音', valid=False)
        items.append(item)
    for index, value in enumerate(result):
        userid = value[2]
        nickname = value[4]
        signature = value[5]
        pinyin = value[6]
        item = alp.Item(title=u'旺旺 \'%s\'' % nickname, subtitle=signature, uid=str(
            index+1), icon='%s%s/CustomHeadImages/%s.jpg' % (path, account, userid), arg='aliim:sendmsg?touid=%s' % userid, valid=True, autocomplete=pinyin)
        items.append(item)
    if len(items) == 0:
        item = alp.Item(title=u'没有查找到匹配好友', valid=False)
        items.append(item)
    alp.feedback(items)


def list_accounts():

    files = os.listdir(path)
    items = []
    for f in files:
        if f.startswith('cn') and os.path.isdir(path + f) and os.path.isfile(path + f + '/db/contact.db'):
            item = alp.Item(title=u'设置帐号 \'%s\'' % f, subtitle='', arg=f, valid=True)
            items.append(item)
    if items.count == 0:
        item = alp.Item(title=u'没有找到可用帐号', subtitle=u'尚未登录过旺旺或者已登录旺旺好友列表已加密', valid=False)
        items.append(item)
    alp.feedback(items)


def set_account(parameter):

    config = open('config', 'w')
    config.write(parameter)
    config.close()


if __name__ == '__main__':
    query('xelz')
    #list_accounts()
