#!/bin/env python
# -*- coding=utf-8 -*-

# /**
# * @file   wx_pay.lib.py
# * @author alvayang <netyang@gmail.com>
# * @date   Fri May 16 17:16:46 2014
# * 
# * @brief  微信支付的Python SDK，当然非官方的，用法见最后
# * 
# * 
# */
'''
'''

import urllib, hashlib
from xml.etree import ElementTree  as ET
import traceback



class WX_PAY_LIB:
    def __init__(self, appid, appkey, appsecret, partner_id, partner_key, verbose = False):
        self.__appid = appid
        self.__charset = 'UTF-8'
        self.__pay_sign_key = appkey
        self.__app_secret  = appsecret
        self.__partner_id = partner_id
        self.__partner_key = partner_key
        self.__verbose = verbose

    def smart_str(self, s, encoding='utf-8', strings_only=False, errors='strict'):
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    return ' '.join([self.smart_str(arg, encoding, strings_only, errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s

    def build_package(self, body, order_id, ip, notify_url, total_fee):
        def _urlrecap(_str):
            return _str.replace("%2f", "%2F").replace("%3a", "%3A")
        debug = False
        # 构造微信请求
        _obj = {}
        _obj['bank_type'] = 'WX'
        _obj['body'] = body
        _obj['partner'] = self.__partner_id
        _obj['out_trade_no'] =  str(_order_id)
        _obj['total_fee'] = str(total_fee)
        _obj['fee_type'] = '1'
        _obj['notify_url'] = notify_url
        _obj['spbill_create_ip'] = ip
        _obj['input_charset'] = self.__charset
        ks = _obj.keys()
        ks.sort()
        newparams = {}
        _string_a= ''
        _string_c = ''
        for k in ks:
            v = _obj[k]
            k = self.smart_str(k, self.__charset)
            newparams[k] = self.smart_str(v)
            if v != '':
                newparams[k] = self.smart_str(v, self.__charset)
                _string_a += '%s=%s&' % (k, newparams[k])
                _string_c += '%s=%s&' % (k, _urlrecap(urllib.quote(v, safe = '')))
        _string_a = _string_a[:-1]
        _string_c = _string_c[:-1]
        _seed = _string_a + '&key=' + self.__partner_key
        if self.__verbose:
            print "[Package Seed]:", _seed
        _string_b = hashlib.md5(_seed).hexdigest().upper()
        _package = _string_c + "&sign=" + _string_b
        return _package

    def sign(self, package, ts, nonceStr = ''):
        debug = False
        _payload = {}
        _payload['appId'] = str(self.__appid)
        _payload['timeStamp'] = str(ts)
        _payload['nonceStr'] = str(nonceStr)
        _payload['appkey'] = str(self.__pay_sign_key)
        _payload['package'] = str(package)
        ks = _payload.keys()
        ks.sort()
        newparams = {}
        _string_a= ''
        for k in ks:
            v = _payload[k]
            k = self.smart_str(k, self.__charset).lower()
            newparams[k] = self.smart_str(v)
            if v != '':
                newparams[k] = self.smart_str(v, self.__charset)
                _string_a += '%s=%s&' % (k, newparams[k])
        _string_a = _string_a[:-1]
        if self.__verbose:
            print "[Sign Seed]:", _string_a
        _payload['package'] = _package
        _payload['paySign'] = hashlib.sha1(_string_a).hexdigest()
        _payload['signType'] = 'SHA1'
        return _payload

    def _valid_sign(ts, noncestr, openid, subscribe):
        _payload = {}
        _payload['appId'] = str(self.__appid)
        _payload['appkey'] = str(self.__pay_sign_key)

        _payload['timeStamp'] = str(ts)
        _payload['nonceStr'] = str(noncestr)
        _payload['issubscribe'] = str(subscribe)
        _payload['openid'] = str(openid)

        ks = _payload.keys()
        ks.sort()
        newparams = {}
        _string_a= ''
        for k in ks:
            v = _payload[k]
            k = self.smart_str(k, self.__charset).lower()
            newparams[k] = self.smart_str(v)
            if v != '':
                newparams[k] = self.smart_str(v, self.__charset)
                _string_a += '%s=%s&' % (k, newparams[k])
        _string_a = _string_a[:-1]
        if self.__verbose:
            print "[PaySign Seed]:", _string_a
        return hashlib.sha1(_string_a).hexdigest()


    def get_dict_from_xml(self, s):
        return_dict = {'OpenId' : '', 'AppId' : '', 'IsSubscribe' : '', 'TimeStamp' : '', 'NonceStr' : '', 'AppSignature' : '', 'SignMethod' : ''}
        try:
            root = ET.fromstring(s)
            for k in return_dict.keys():
                try:
                    if self.__verbose:
                        print "[LookingFor]:", k
                    return_dict[k] = _appsignature = root.find(k).text
                except:
                    if self.__verbose:
                        print traceback.format_exc()
        except:
            if self.__verbose:
                print traceback.format_exc()
            pass
        return return_dict;



if __name__ == "__main__":
    # 下列参数源自于微信官方demo中的参数。
    # https://mp.weixin.qq.com/htmledition/res/bussiness-course2/wxm-pay-api-demo.zip

    appid = 'wxf8b4f85f3a794e77'
    pay_sign_key = '2Wozy2aksie1puXUBpWD8oZxiD1DfQuEaiC7KcRATv1Ino3mdopKaPGQQ7TtkNySuAmCaDCrw4xhPY5qKTBl7Fzm0RgR3c0WaVYIXZARsxzHV2x7iwPPzOz94dnwPWSn'
    app_secret = 'aa7171b26a15a20085ba0ca0bcfb0cb0'
    partner_id = '1900000109'
    partner_key = '8934e7d15453e97507ef794cf7b0519d'

    _s = '<xml><OpenId><![CDATA[o_pu7uL0-CqaPQDgg6N4JEzl0qHY]]></OpenId>\n<AppId><![CDATA[wx8699235240b50cd6]]></AppId>\n<IsSubscribe>1</IsSubscribe>\n<TimeStamp>1400152639</TimeStamp>\n<NonceStr><![CDATA[BtMQxyEhJWuD9e96]]></NonceStr>\n<AppSignature><![CDATA[532b48bf2960f659131d7bfbbffd9a970a07ed6a]]></AppSignature>\n<SignMethod><![CDATA[sha1]]></SignMethod>\n</xml>'

    t = WX_PAY_LIB(appid, pay_sign_key, app_secret, partner_id, partner_key, True)
    d = t.get_dict_from_xml(_s)
    _ts = '1400230151064'
    _nonestr = 'p4nolFgn6IzgXa4qTHLAeEP6stKVwgfi'
    _notify_url = "http://www.qq.com"
    _body = '江诗丹顿'
    _order_id = '22634595771530777000'
    _ip = "127.0.0.1"
    _total_fee = 1
    _package = t.build_package(_body, _order_id, _ip, _notify_url, _total_fee);
    _sign  = t.sign(_package, _ts, _nonestr)

    print _package, _sign
