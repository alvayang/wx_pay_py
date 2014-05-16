wx_pay_py
=========

微信支付辅助类


用法也是超简单了:

     t = WX_PAY_LIB(appid, pay_sign_key, app_secret, partner_id, partner_key, True)
     # 构造Package
     _package = t.build_package(_body, _order_id, _ip, _notify_url, _total_fee)
     # 对Package签名
     _sign  = t.sign(_package, _ts, _nonestr)
     
     # 当微信返回过来交易结果的时候，使用
     d = t.get_dict_from_xml(_s)
     # 这时候  d(dict) 里面就包含了
     #  {'OpenId' : '', 'AppId' : '', 'IsSubscribe' : '', 'TimeStamp' : '', 'NonceStr' : '', 'AppSignature' : '', 'SignMethod' : ''}
     # 然后可以拿着这个，继续做签名:
     _vsign = t.valid_sign(d['TimeStamp'], d['NonceStr'], d['OpenId'], d['IsSubscribe'])
     # 然后就可以对比d['AppSignature'] 和 _vsign了

参数的含义参考官方文档。
