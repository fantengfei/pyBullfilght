# coding=UTF-8
import urllib
import random, string, json
import sqldb

def check_session(data):
    re = sqldb.query_db('select session from login where openid = ?', [data['openid']], one=True)
    if re != None and re.get('session') == data['session']:
        return True
    return False

def make_session(code):
    # https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    # AppID: wxe2018d200c505930
    # appsecret: be695b45f2b697ab837bd992baa8f676

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxe2018d200c505930&secret=be695b45f2b697ab837bd992baa8f676&js_code=' + code + '&grant_type=authorization_code'
    result = urllib.urlopen(url)
    j = json.load(result)
    
    session_key = ''.join(random.sample(string.ascii_letters, 32))
    openid = j['openid']

    if session_key and openid:
        re = sqldb.query_db('select * from login where openid = ?', [openid], one=True)

        if re == None:
            print 'insert' + openid
            res = sqldb.query_db('insert into login(openid, session) values(?, ?)', [openid, session_key])
        else:
            print 'update' + openid
            res = sqldb.query_db('update login set session = ? where openid = ?', [session_key, openid])

        return {'openid': openid, 'session':session_key}

    return False
        