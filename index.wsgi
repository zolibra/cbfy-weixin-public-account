#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import sae
import web
import model

urls = (
    '/', 'Index',
	'/test', 'Test',
	'/weixin', 'Weixin'
)

application = app = web.application(urls, globals()).wsgifunc()
render = web.template .render('templates/' )

class Test:
    #Test
    def GET(self):
        return u'你好'

class Index:
    #redirect to index.html
    def GET(self):
        return render.index()

class Weixin:
    #handle auth request from weixin
    def GET(self):
        data = web.input()
        return model.handleAuthentication(data)
    #handle POST message from weixin	
    def POST(self):
        data = web.input()
        return model.handlePostMessage(data)


if __name__ == "__main__":
    web.application(urls, globals()).run()
'''    
class CleanDB_TestCase(unittest.TestCase):
    def setUp(self):
        dba.del_allgames()
        dba.del_allusers()

#test keyword bm                
class Apply_New_User_TestCase(CleanDB_TestCase):
    def runTest(self):
        print '---->Apply_New_User_TestCase<----------'
        dba.insert_userinfo('ray123', 'ray', 0)
        dba.insert_game(int(time.time()), 'chaoyang', '2013-5-1', '14:00:00')
        ct = str(int(time.time()))
        raw = TEXT_MSG_TPL % ('cbfy', 'rray123', ct, 'bm ray')
        msg = passContent(raw)
        handleRule(msg)
        user = dba.get_username(str('rray123'))
        print user
        self.assertEqual(user.name, [''])
        print '<----Apply_New_User_TestCase----------->'

        
class Apply_Exist_User_TestCase(CleanDB_TestCase):
    def runTest(self):
        dba.insert_userinfo('ray123', 'ray', 0)
        ct = str(int(time.time()))
        dba.insert_game(ct, 'chaoyang', '2013-5-1', '14:00:00')
        raw = TEXT_MSG_TPL % ('cbfy', 'ray123', str(int(time.time())), 'bm ray')
        msg = passContent(raw)
        handleRule(msg)
        user = dba.get_username(str('ray123'))
        self.assertEqual(user.name, 'ray')
        
class Create_Game_TestCase(CleanDB_TestCase):
    def runTest(self):
        print '---->Create_Game_TestCase<----------'
        raw = TEXT_MSG_TPL % ('cbfy', 'ray123', str(int(time.time())), 'cj chaoyang 2013-05-01 14:00:00')
        msg = passContent(raw)
        handleRule(msg)
        gamelist = dba.get_allgames()
        list = []
        for game in gamelist:
            list.append(game)
        self.assertEqual(list[0].location , 'chaoyang')
        #need force to str here
        self.assertEqual(str(list[0].date) , u'2013-05-01')
        self.assertEqual(str(list[0].time) , '14:00:00')     
        print '<----Create_Game_TestCase----------->'

class ShowGame_TestCase(CleanDB_TestCase):
    def runTest(self):
        print '---->ShowGame_TestCase<----------'
        dba.insert_game(int(time.time()), 'chaoyang', '2013-5-1', '14:00:00')
        time.sleep(1)
        dba.insert_game(int(time.time()), 'Haidian', '2013-12-11', '14:00:00')
        raw = TEXT_MSG_TPL % ('cbfy', 'ray123', str(int(time.time())), Keyword['showgame'] + ' chaoyang 2013-05-01 14:00:00')
        msg = passContent(raw)
        print handleRule(msg)
        print '<----ShowGame_TestCase----------->'
'''
        




