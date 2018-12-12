#!/usr/bin/python2.7

import MySQLdb

def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='dkarroyo',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn

def get_perms(cid, campid, kind, conn):
    '''
    Input: -cid, or the primary key of the object
           -campid, or the id of the current campaign
           -kind, either "notes", "misc", "character", or "towns"
           -conn, a database connection
    Output: A dictionary containing two dictionaries. One has each user in campaign,
            where the user's id is the key and the user's name is the value. The 
            other dict is similar, but only has users with current permission to 
            veiw an item. Note that the list of users with permission does not 
            include the DM or the creator, who can always view the item. 
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    current_perms = {}
    
    #get all users in the campaign
    num_rows = curs.execute("select * from usertocamp where cid=%s",(campid,))
    all_users = []
    gm = None
    if num_rows!=0:
        for elt in curs.fetchall():
            if elt["dm"]=="yes":
                gm=elt["uid"]
            if gm!=elt["uid"]:
                all_users.append(elt["uid"])
    
    #get all users with current permissions, not including DM
    num_rows = curs.execute("select uid from usercomp where cid=%s and comptype=%s", 
        (cid, kind))
    allowed = []
    if num_rows!=0:
        for elt in curs.fetchall():
            allowed.append(elt["uid"])
            
    #get creator of the item 
    if kind=="character":
        num_rows = curs.execute('''select uid from `character` where cid=%s''', (cid,))
    elif kind=="notes":
        num_rows = curs.execute('''select uid from notes where nid=%s''', (cid,))
    elif kind=="towns":
        num_rows = curs.execute('''select uid from towns where tid=%s''', (cid,))
    else:
        num_rows = curs.execute('''select uid from misc where mscid=%s''', (cid,))
    creator = curs.fetchone()["uid"]
    
    #remove the creator from the permissions list
    try:
        all_users.remove(creator)
    except:
        pass
    
    #get the the user names for the users in the campaign, make the all player
    #dict
    all_dict = {}
    for player in all_users:
        curs.execute('''select username from user where uid=%s''', (player,))
        player_name = curs.fetchone()
        all_dict[player] = player_name["username"]
    
    #create a dict with only players that currenlty have permission
    allowed_dict = {} 
    for player in allowed:
        if player in all_users:
            allowed_dict[player] = all_dict[player]
    
    current_perms["allowed"] = allowed_dict
    current_perms["all"] = all_dict
    
    return current_perms

def get_all(uid, campid, conn):
    '''
    Input: -uid, or current user in the session
           -campid, or the id of the current campaign
           -conn, a database connection
    Output: A dictionary containing a list of dictionaries for each type of item.
            This includes "notes", "characters", "towns", "files", and any other 
            user created misc types. The sub-dictionaries contain information for 
            each item, including the id of item, the name of the item, the creator 
            of the item, the permissions on the item, an associated file name, etc. 
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    #get dm for campaign
    curs.execute('''select * from usertocamp where uid=%s and cid=%s''',(uid,campid))
    camps = curs.fetchone()
    is_dm = False
    if camps["dm"]=="yes":
        is_dm = True  
    
    #dict of types to return
    all = {}
    
    #get items that the user has access to for all types
    for col in ["`character`", "notes", "towns", "misc"]:

        all_access = []  
        #if the user in the DM, allow them to have access to all elements in the
        #campaign
        if is_dm==True:
            if col=="`character`":
                curs.execute('''select * from `character` where campid=%s''',(campid,))
            elif col=="notes":
                curs.execute('''select * from notes where campid=%s''',(campid,))
            elif col=="towns":
                curs.execute('''select * from towns where campid=%s''',(campid,))
            else:
                curs.execute('''select * from misc where campid=%s''',(campid,))
            all_access = list(curs.fetchall())
        #if the user is not the DM, get items that the user made
        else:
            num_rows = None
            if col=="`character`":
                num_rows = curs.execute('''select * from `character`
                where uid=%s and campid=%s''', (uid,campid))
            elif col=="notes":
                num_rows = curs.execute('''select * from notes 
                where uid=%s and campid=%s''', (uid,campid))
            elif col=="towns":
                num_rows = curs.execute('''select * from towns 
                where uid=%s and campid=%s''', (uid,campid))
            else:
                num_rows = curs.execute('''select * from misc
                where uid=%s and campid=%s''', (uid,campid))
            
            #add all items that the user created to the dictionary list
            if num_rows!=0:
                all_access.extend(list(curs.fetchall()))
            
            #if the user is not the DM, get items that the user has been granted
            #access to 
            if col=="`character`":
                num_rows = curs.execute('''select * from `character`,usercomp 
                where campid=%s and usercomp.uid=%s and usercomp.comptype="character"
                and usercomp.cid=`character`.cid''',
                (campid,uid))
            elif col=="notes":
                num_rows = curs.execute('''select * from notes,usercomp 
                where campid=%s and usercomp.uid=%s and usercomp.comptype="notes"
                and usercomp.cid=notes.nid''',
                (campid,uid))
            elif col=="towns":
                num_rows = curs.execute('''select * from towns,usercomp 
                where campid=%s and usercomp.uid=%s and usercomp.comptype="towns"
                and usercomp.cid=towns.tid''',
                (campid,uid))
            else:
                num_rows = curs.execute('''select * from misc,usercomp 
                where campid=%s and usercomp.uid=%s and usercomp.comptype="misc"
                and usercomp.cid=misc.mscid''',
                (campid,uid))
            
            #add all items that the user created to the dictionary list
            if num_rows!=0:
                all_access.extend(list(curs.fetchall()))
        #add all item type lists to the main access dictionary          
        all[col] = all_access
        
    kinds = {}
    #get all kinds of misc items
    for elt in all["misc"]:
        if elt["kid"] not in kinds.keys():
            curs.execute("select * from kind where kid=%s",[elt["kid"]])
            kinds[elt["kid"]] = curs.fetchone()["name"]
    
    #create dict entries for all items (list of subdicts for each misc type)
    for elt in all["misc"]:
        if kinds[elt["kid"]] in all.keys():
            new_list = all[kinds[elt["kid"]]].append(elt)
            all[kinds[elt["kid"]]] = new_list
        else: 
            all[kinds[elt["kid"]]] = [elt]
    
    #delete main misc type
    del all["misc"]
    
    #change `character` to character (because "character" is a reserved MySQL
    #word)
    all["character"] = all["`character`"]
    del all["`character`"]
    
    #for each type, add "cid" equal to whatever it was called from the database
    #(I can change this to be done in the query), and add the dict of permissions
    for kind in all.keys():
        if kind=="character":
            curr_cid = "cid"
            url_key = "cid"
        elif kind=="notes":
            curr_cid = "nid"
            url_key = "nid"
        elif kind=="towns":
            curr_cid = "tid"
            url_key = "tid"
        else:
            curr_cid = "mscid"
            url_key = "mscid"
        for obj in all[kind]:
            obj["perms"] = get_perms(obj[curr_cid], campid, kind, conn)
            obj["cid"] = obj[curr_cid]
    
    #capatilize all kind names for presentation (could also be done in SQL 
    #statements)
    for kind in all.keys():
        new_kind = kind.capitalize()
        if new_kind!=kind:
            all[new_kind] = all[kind]
            del all[kind]

    return all
    
def add_type(new_type, campid, conn):
    '''
    Input: -new_type, new type to be added to campaign
           -campid, id of campaign type is to be added to  
           -conn, a database connection
    Output: "true" this update was successful, or "false", this update was not 
            succcessful because type already exists. 
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #try to insert new type into the campaign
    try:
        curs.execute('''insert into kind(name)
                    values(%s)''',[new_type])
        #if successful, return true to flask app
        return True
    #if type already exists, return false to flask app
    except MySQLdb.IntegrityError:
        return False

def camp_name(cid, conn):
    '''
    Input: -cid, or current campaign id in session
           -conn, a database connection
    Output: The name of the current campaign in the session 
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from campaign where cid=%s''',(cid,))
    return curs.fetchone()["name"]

def change_perms(cid, perms_list, non_perms_list, campid, kind, conn):
    '''
    Input: -cid, or primary key of object
           -perms_list, list of users that should get access
           -non_perms_list, list of users that should not have permission
           -campid, id of current campaign in session
           -kind, the type of object
           -conn, a database connection
    This function changes the permissions in the database to those checked on the
    main campaign page. 
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    for user in perms_list:
        #if user does not have permission, add to permission table
        curs.execute('''insert into usercomp values (%s,%s,%s)
            on duplicate key update uid=%s''', (cid, user, kind, user))
    for user in non_perms_list:
        #if user in non_perms_list has permission, delete 
        curs.execute('''delete from usercomp where uid=%s and cid=%s
            and comptype=%s''', (user,cid,kind))

def all_users(camp_id, conn):
    '''
    Input: -kind, the type of object
           -conn, a database connection
    Output: This function gives a list of all users curently in the campaign.   
    '''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) 
    curs.execute('''select uid from usertocamp where cid=%s''', (camp_id,))
    all_use = curs.fetchall()
    to_ret = []
    for elt in all_use:
        to_ret.append(elt["uid"])
    return to_ret

if __name__ == '__main__':
    conn = getConn("pbmod")
    
    #testing get_all
    #test for gm 
    print(get_all(1, 1, conn))
    
    #test for non-gm
    print(get_all(6, 1, conn))
    
    #testing get_perms
    #test for character
    print(get_perms(1,1,"character",conn))
    
    #testing change_perms
    change_perms(1,[3],[2],1,"character",conn)
    
    print(get_perms(1,1,"character",conn))
    
    #testing all_users
    print(all_users(1, conn))