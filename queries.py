import MySQLdb
import sys

#encoding: utf-8

def getConn(db):
    conn= MySQLdb.connect(host='localhost',
                           user='dkarroyo',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn
    
def getUserCampaigns(conn,uid,rowType = 'dictionary'):
    '''Get all campaigns user is affiliated with'''
    if rowType == 'tuple':
        curs = conn.cursor()
    elif rowType == 'dictionary':
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select campaign.name as name, campaign.cid as cid 
                    from user inner join usertocamp using (uid) 
                    inner join campaign using (cid) 
                    where uid = %s;''',[uid])
    return curs.fetchall()
    
def registerUser(conn,username,passwd,rowType='dictionary'):
    '''Register new user and return their uid.
    Return False if username already exists.'''
    if rowType == 'tuple':
        curs = conn.cursor()
    elif rowType == 'dictionary':
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        
    curs.execute('''select * from user where username = %s''',[username])
    if curs.fetchone() is not None:
        return False
    
    curs.execute('''insert into user(username,hashed) values (%s,%s)''',
                [username,passwd])
    
    curs.execute('''select last_insert_id()''')
    
    return curs.fetchone()['last_insert_id()']
    
def createCampaign(conn,campName):
    '''Add new campaign to database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into campaign(name) values (%s)''',[campName])
    curs.execute('''select last_insert_id()''')
    
    return curs.fetchone()['last_insert_id()']
    
def getUserID(conn,username):
    '''Return a username\'s associated uid'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select uid from user where username = %s''',[username])
    return curs.fetchone()
    
def addPlayerToCamp(conn,uid,cid,dm = 'no'):
    '''Adds a player to a campaign.'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''insert into usertocamp(dm,cid,uid) values(%s,%s,%s) 
                    on duplicate key update uid=uid''',
                    [dm,cid,uid])
                    
def getCampPlayers(conn,cid):
    '''Returns the usernames of all players associated with a campaign in (nested) tuple form'''
    
    curs = conn.cursor()
    curs.execute('''select username from user 
                    inner join usertocamp using (uid) 
                    inner join campaign using (cid) where cid = %s''',[cid])
                    
    return curs.fetchall()
    
def userIsDM(conn,uid,cid):
    '''Return True if given uid is the dm of given cid'''
    curs = conn.cursor()
    curs.execute('''select dm from usertocamp where cid = %s and uid = %s''',[cid,uid])
    
    try:
        dm = curs.fetchone()[0]
    except:
        return False
    
    if dm == 'yes':
        return True
    
    return False
    
def removePlayer(conn,uid,cid):
    '''Remove given user from given campaign'''
    curs = conn.cursor()
    curs.execute('''delete from usertocamp where uid = %s and cid = %s''',[uid,cid])