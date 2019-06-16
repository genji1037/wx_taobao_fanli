# encoding: utf-8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@license: Apache Licence
@file: wx_bot.py
@time: 2017/5/28 上午10:40

"""
from __future__ import unicode_literals

import platform
import re
import sys
import threading
import traceback

import itchat
import requests
from itchat.content import *
from libs import utils
from libs import model
from libs.alimama import Alimama

logger = utils.init_logger()

al = Alimama(logger)
res = al.login()
if res == "login failed":
    sys.exit(0)


# 检查是否是淘宝链接
def check_if_is_tb_link(msg):
    if re.search(r'【.*】', msg.text) and (
            u'打开👉手机淘宝👈' in msg.text or u'打开👉天猫APP👈' in msg.text or u'打开👉手淘👈' in msg.text or u'👉淘♂寳♀👈' in msg.text):
        try:
            logger.debug(msg.text)
            q = re.search(r'【.*】', msg.text).group().replace(u'【', '').replace(u'】', '')
            if u'打开👉天猫APP👈' in msg.text:
                try:
                    url = re.search(r'https://.* ', msg.text).group()
                except:
                    url = None
                    taokouling = re.search(r'￥.*?￥', msg.text).group()
            elif u'👉淘♂寳♀👈' in msg.text:
                try:
                    url = re.search(r'https://.* ', msg.text).group()
                except:
                    url = None
                    taokouling = re.search(r'€.*?€', msg.text)

            else:
                try:
                    url = re.search(r'https://.* ', msg.text).group()
                except:
                    url = None
            # 20170909新版淘宝分享中没有链接， 感谢网友jindx0713（https://github.com/jindx0713）提供代码和思路，现在使用第三方网站 http://www.taokouling.com 根据淘口令获取url
            if url is None:
                taokoulingurl = 'http://www.taokouling.com/index.php?m=api&a=taokoulingjm'
                parms = {'username': 'wx_tb_fanli', 'password': 'wx_tb_fanli', 'text': taokouling}
                res = requests.post(taokoulingurl, data=parms)
                url = res.json()['url'].replace('https://', 'http://')
                info = "tkl url: {}".format(url)
                logger.debug(info)
                if url == "":
                    info = u'''%s
                    -----------------
                    该宝贝暂时没有找到内部返利通道！亲您可以换个宝贝试试。
                                ''' % q
                    msg.user.send(info)
                    return

            # get real url
            real_url = al.get_real_url(url)
            info = "real_url: {}".format(real_url)
            logger.debug(info)

            # get detail
            res = al.get_detail(real_url)
            auctionid = res['auctionId']
            coupon_amount = res['couponAmount']
            tk_rate = res['tkRate']
            price = res['zkPrice']
            fx = (price - coupon_amount) * tk_rate / 100

            # 分配fx
            user_fx = round(fx / 2 * 100) / 100
            robot_fx = fx - user_fx

            # find user
            itchat.get_friends(update=True)
            user = itchat.search_friends(userName=msg['FromUserName'])
            if user is None:
                print('not friend yet add user %s' % msg['FromUserName'])
                itchat.add_friend(msg['FromUserName'])
            uid = user['RemarkName']

            if (isinstance(uid, int) and uid > 0) or (isinstance(uid, str) and len(uid) > 0):
                # 该用户已经备注过
                # 检查用户是否在数据库里
                res1 = al.get_tk_link(auctionid, '')

            else:  # new user create it
                print('set new alias')
                # 新用户需要绑定推广位
                # 查询现存的free推广位
                # free_adzones = model.Adzone.select().where(model.Adzone.state == 'free')
                # cnt = free_adzones.count()
                # if cnt == 0:
                #     # 没有free推广位,则创建推广位并入库
                #     adzone_info = al.create_adzone()
                #     adzone_id = adzone_info['adzone_Id']
                #     model.Adzone.create(adzone_id=adzone_id, state='bind')
                # else:
                #     adzone_id =free_adzones[1]['adzone_Id']

                # res1 = al.get_tk_link(auctionid, adzone_id)
                res1 = al.get_tk_link(auctionid, '')

                user_model = model.User.create(balance='0', total_amt='0', adzone_id='')
                uid = user_model.id
                itchat.set_alias(user['UserName'], uid)

            tao_token = res1['taoToken']
            short_link = res1['shortLinkUrl']
            coupon_link = res1['couponLink']
            if coupon_link != "":
                coupon_token = res1['couponLinkTaoToken']
                res_text = '''
%s
【返现】%.2f
【优惠券】%s元
请复制%s淘口令、打开淘宝APP下单
-----------------
【下单地址】%s
                ''' % (q, user_fx, coupon_amount, coupon_token, short_link)
            else:
                res_text = '''
%s
【返现】%.2f元
【优惠券】%s元
请复制%s淘口令、打开淘宝APP下单
-----------------
【下单地址】%s
                                ''' % (q, user_fx, coupon_amount, tao_token, short_link)

            msg.user.send(res_text)
        except Exception as e:
            trace = traceback.format_exc()
            logger.warning("error:{},trace:{}".format(str(e), trace))
            info = u'''%s
-----------------
该宝贝暂时没有找到内部返利通道！亲您可以换个宝贝试试。
            ''' % q
            msg.user.send(info)


class WxBot(object):
    @itchat.msg_register([TEXT])
    def text_reply(msg):
        print(msg.text)
        check_if_is_tb_link(msg)
        # msg.user.send('%s: %s' % (msg.type, msg.text))

    @itchat.msg_register(TEXT, isGroupChat=True)
    def text_reply(msg):
        check_if_is_tb_link(msg)
        # if msg.isAt:
        #     msg.user.send(u'@%s\u2005I received: %s' % (
        #         msg.actualNickName, msg.text))

    def run(self):
        sysstr = platform.system()
        if (sysstr == "Linux") or (sysstr == "Darwin"):
            # itchat.auto_login(enableCmdQR=2, hotReload=True)
            itchat.auto_login(hotReload=True)
        else:
            itchat.auto_login(hotReload=True)
        itchat.run(True)


if __name__ == '__main__':
    mi = WxBot()
    t = threading.Thread(target=mi.run, args=())
    t.start()
