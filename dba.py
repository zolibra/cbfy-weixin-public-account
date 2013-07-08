#!/bin/env python
# -*- coding: utf-8 -*- 
import web
import unittest
import time
import myconf

db = web.database(dbn='mysql',host=myconf.MYSQL_HOST_M, port=myconf.MYSQL_PORT,db=myconf.MYSQL_DB, user=myconf.MYSQL_USER, pw=myconf.MYSQL_PASS)


#USERINFO operation
def get_username(id):
    iterater = db.select(myconf.DB_USERINFO_TABLE_NAME, where='user_id=$id',vars=locals())
    list = []
    copy2array(iterater, list)
    if list:
        return list[0]
    else:
        return ''

def get_allusers():
    return db.select(myconf.DB_USERINFO_TABLE_NAME, where="user_id!=-1", vars=locals())

def get_usersbygameid(id):
    iterater = db.select(myconf.DB_USERINFO_TABLE_NAME, where="game_id=$id", vars=locals())
    list = []
    copy2array(iterater, list)
    if list:
        namelist = []
        output = ','
        for i in list:
            namelist.append(i.name)
        return output.join(namelist)
    else:
        return ''

def insert_userinfo(id, na, gid):
    db.insert(myconf.DB_USERINFO_TABLE_NAME, user_id=id, name=na, game_id=gid)

def update_usergame(id, na, gid):
    db.update(myconf.DB_USERINFO_TABLE_NAME, where='user_id=$id',game_id=gid, vars=locals())

def del_user_info(id):
    db.delete(myconf.DB_USERINFO_TABLE_NAME, where="user_id=$id", vars=locals())

def del_allusers():
    db.delete(myconf.DB_USERINFO_TABLE_NAME, where="user_id!=-1", vars=locals())

#Game operation
def get_game(id):
    return db.select(myconf.DB_GAME_TABLE_NAME, where='id='+id)

def get_allgames():
    return db.select(myconf.DB_GAME_TABLE_NAME, where="id!=-1", vars=locals())

def get_latestgames():
    iterater = db.select(myconf.DB_GAME_TABLE_NAME, order='date desc', limit='1',vars=locals())
    list = []
    copy2array(iterater, list)
    if list:
        return list[0]
    else:
        return ['']
    
def insert_game(id, l, d, t):
    db.insert(myconf.DB_GAME_TABLE_NAME, id=id, location=l, date=d , time=t)

def del_game_by_id(id):
    db.delete(myconf.DB_GAME_TABLE_NAME, where="id=$id", vars=locals())
    
def del_allgames():
    db.delete(myconf.DB_GAME_TABLE_NAME, where="id!=-1", vars=locals())

def copy2array(it , l):
    print it
    for i in it:
        l.append(i)
    return l


'''        
class UserInfoInsertTestCase(unittest.TestCase):
    def runTest(self):
        del_allusers()
        insert_userinfo('1', 'bob', 0)
        insert_userinfo('2', 'jim' , 0)
        userlist = get_allusers()
        #python iter can only iterate once , so create a list and copy the content
        list = []
        for user in userlist:
            list.append(user)
        self.assertEqual(list[0].user_id , u'1')
        self.assertEqual(list[0].name , 'bob')
        self.assertEqual(list[0].game_id , 0)        
class GameTestCase(unittest.TestCase):
    def runTest(self):
        del_allgames()
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        t = time.strftime('%H:%M:%S',time.localtime(time.time()))
        insert_game(1 , 'Chaoyang' , date , t)
        gamelist = get_allgames()
        list = []
        for game in gamelist:
            list.append(game)
        
        self.assertEqual(list[0].id , 1)
        self.assertEqual(list[0].location , 'Chaoyang')
        #need force to str here
        self.assertEqual(str(list[0].date) , date)
        self.assertEqual(str(list[0].time) , t)
        
        #test query, the get_game still return a list
        gamelist = get_game('1')
        list2 = []
        for game in gamelist:
            list2.append(game)
        self.assertEqual(list2[0].location, 'Chaoyang')
        self.assertEqual(str(list2[0].date) , date)
        self.assertEqual(str(list2[0].time) , t)
        
        #test latest game, on 12-10, we will play the game as haidian:)
        insert_game(2 , 'Haidian' , '2013-12-10' , t)
        game2 = get_latestgames()
        print game2[0].location
        return
    
class GetUserTestCase(unittest.TestCase):
        del_allusers()
        insert_userinfo('1', 'bob', 0)
        insert_userinfo('2', 'jim' , 0)
        user_id = get_username('3')
        if user_id:
            print "exist"
        else: 
            print "not exist"

'''