#!/usr/bin/python
#coding=utf-8
"""
    douban_group_sofa_bot
    Copyright (C) 2011  Meng Zhuo <mengzhuo1203@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import urllib
import urllib2
import cookielib
import re
import time
import random
from datetime import datetime

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
    
def post(url,data,cj):
	req = urllib2.Request(url)
	data = urllib.urlencode(data)
	#enable cookie	
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	response = opener.open(req, data)
	#DEBUG AREA
	if debug >= 1:
	    print 'POST_REQUEST:\n'+url
	    print 'POST_CONTENT:\n'+data
	    #print 'POST_RESPONSE:\n'+replace_all(response.read(),{'\n':'','\t':'',' ':'','　':''})
	return response.read()
	
def browse(url,cj):
    req = urllib2.Request(url)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    response = opener.open(req)
    if debug > 4:
	    print 'BROSWE_REQUEST:\n'+url
	    print 'BROSWE_RESPONSE:\n'+response.read()
    return response.read()
    
def main():
    du = 'http://m.douban.com'
    #设置区域
    #set Group ID
    group_id = 'fsm'
    #set refresh_interval
    refresh_interval = 1
    #set sofa Content
    sofa_content = '今晚沙发都是我的啦，B友们不要嫉妒啊\nby:俺的PYTHON机器人'
    data = {'form_email':'mengzhuo1203@gmail.com', 'form_password':'abcdefg', 'action':'/'}
    #到这就不要修改了，除非你知道你在干吗
    
    #FIXME Why need one more Login, wired?
    if browse(du,cj)
    
    
    #login
    try:
        post(du, data,cj)
    except:
        print 'FATAL'
        exit(0)
    times = 0       
    while True:
        #Get Groups
        group_content = browse(du+'/group/'+group_id+'/',cj)
        replace_dict = {'\n':'','\t':'',' ':'','　':''}
        group_content = replace_all(group_content,replace_dict)
        if debug >=1:
            print group_content
        if times == 0:
            group_title = re.findall('<title>(.*)<\/title>',group_content)[0]
            print '\n-----抢"'+group_title+'"的沙发中-----'
            times+=1
        items = re.findall('ahref="\/group\/topic\/(\d+)\/\?session=\w+">([^<]+)<\/a><span>\|',group_content)
       
        if not items.__len__() == 0:
            #print items
            for i in items:
                item_title = i[1]
                item_ID = i[0]
                print '标题:'+item_title+'[沙发@'+datetime.now().isoformat()+']\n'
                item_url = du+'/group/topic/'+item_ID+'/'
                item_content = browse(item_url,cj)
                if not re.match('captcha',item_content):
                    item_post_session = re.findall('name="session"value="([^"]+)"',replace_all(item_content,replace_dict))
                    #print item_post_session
                    item_post_session = item_post_session[0]
                    data = {'content':sofa_content,'action':'comments','session':item_post_session}
                    post(item_url+'comments',data,cj)
                else:
                    print '有验证码啦！\a'
                    break
        if debug ==1:
            time.sleep(refresh_interval)
        else:
            time.sleep(refresh_interval*random.randint(1,5))

            
            

if __name__ == '__main__':
    cj = cookielib.CookieJar()
    debug = 1
    main()
