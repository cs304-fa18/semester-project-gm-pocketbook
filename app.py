from flask import (Flask, url_for, render_template, request, redirect, session,flash, jsonify)
import pb_view, queries
import MySQLdb
import bcrypt
 
app = Flask(__name__)

app.secret_key = 'secret'

DATABASE = 'pbmod'

@app.route('/',methods=['GET','POST'])
def home():
    '''Home page method. Displays welcome message or login page.'''
    if request.method == 'GET':
        #check if logged in
        if 'uid' in session:
            # get user info
            username = session['username']
            uid = session['uid']
            conn = queries.getConn(DATABASE)
            campaigns = queries.getUserCampaigns(conn,uid)
            
            #render template
            return render_template('home.html',username = username, campaigns = campaigns)
        else:
            # render template w/o user info
            username = None
            campaigns = None
            return render_template('home.html',username = username, campaigns = campaigns)
    else: #login attempt
        user = request.form.get('user')
        attempt = request.form.get('password')
        
        # check database for user-pass match
        conn = queries.getConn(DATABASE)
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        
        curs.execute('''select hashed from user where username = %s''',
                    [user])
                    
        password = curs.fetchone()
        if password is None:
            flash("Login unsuccessful. Try again.")
            return redirect(url_for('home'))
        
        hashed = password['hashed']
        
        if bcrypt.hashpw(attempt.encode('utf-8'),hashed.encode('utf-8')) == hashed:
            session['username'] = user
            
            #get uid
            curs.execute('''select uid from user where username = %s''',
                                [user])
            uid = curs.fetchone()['uid']
            session['uid'] = uid
            flash("Login successful for " + user)
            return redirect(url_for('home'))
        
        else:
            flash("Login unsuccessful. Try again.")
            return redirect(url_for('home'))
            
@app.route('/setCamp/',methods=['POST'])
def setCamp():
    if request.method == 'POST':
        session['camp'] = request.form.get('campid')
        return redirect(url_for('campPage'))

@app.route('/register/',methods=['GET','POST'])
def register():
    '''User registration route.'''
    if request.method == 'GET':
        if 'uid' in session:
            flash('Already logged into existing account.')
            return redirect(url_for('home'))
        else:
            return render_template("register.html")
    else: #submit registration form
        username = request.form.get('user')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
        
        if pass1 != pass2:
            flash("Passwords don't match")
            return redirect(url_for('register'))
        
        else: #register user into database
            hashed = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt())
            conn = queries.getConn(DATABASE)
            try:
                uid = queries.registerUser(conn,username,pass1)
            except:
                flash("There was an error registering user")
                return redirect(url_for("register"))
            if uid == False:
                flash("User already exists")
                return redirect(url_for("register"))
            else:
                session['uid'] = uid
                session['username'] = username
                flash("Registration successful")
                return redirect(url_for("home"))
                
@app.route('/logout/',methods = ['GET','POST'])
def logout():
    '''Route to log out current user'''
    if 'uid' in session:
        session.pop('uid')
        session.pop('username')
        flash("Successfully logged out")
        return redirect(url_for('home'))
    else:
        flash('You are not logged in.')
        return redirect(url_for('home'))
        
@app.route('/newCamp/', methods=['GET','POST'])
def newCamp():
    if 'uid' not in session: #verify user is logged in
        flash("Login to add campaign.")
        return redirect(url_for('home'))
        
    if request.method == 'GET': #display form
        return render_template('new_camp.html')
    else:
        uid = session['uid']
        campName = request.form.get("name")
        players = request.form.get("players")
        players = players.strip().split() #make into list
        
        conn = queries.getConn(DATABASE)
        
        #insert new campaign into db
        cid = queries.createCampaign(conn,campName)
        
        #insert players into campaign
        for player in players:
            playerID = queries.getUserID(conn,player)
            if playerID == None:
                flash("There was an error adding "+player+" to campaign.")
            else:
                try:
                    queries.addPlayerToCamp(conn,playerID['uid'],cid)
                except:
                    flash("There was an error adding "+player+" to campaign.")
            
        #insert current user as dm to campaign (assume only DMs are creating campaigns)
        queries.addPlayerToCamp(conn,uid,cid,dm = 'yes')
        
        session['camp'] = cid
        return redirect(url_for('campPage'))
        
@app.route('/editPlayers/',methods = ['GET','POST'])
def editPlayers():
    if 'uid' in session and 'camp' in session:
        uid = session['uid']
        cid = session['camp']
        
        conn = queries.getConn(DATABASE)
        
        if not queries.userIsDM(conn,uid,cid):
            flash("You cannot add or remove players.")
            return redirect(url_for('campPage'))
        
        if request.method == 'GET':
            name = pb_view.camp_name(cid, conn)
            players = map(lambda x: x[0],queries.getCampPlayers(conn,cid)) #get campaign players and clean list
            return render_template('edit_players.html',name = name, players = ' '.join(players))
            
        else:
            playersBefore = map(lambda x: x[0],queries.getCampPlayers(conn,cid))
            players = request.form.get("players")
            players = players.strip().split() #make into list
            
            #Remove players who've been removed
            for player in playersBefore: #this is horrible and i hate it
                if player not in players:
                    queries.removePlayer(conn,queries.getUserID(conn,player)['uid'],cid)
            
            #insert players into campaign
            for player in players:
                playerID = queries.getUserID(conn,player)
                if playerID == None:
                    flash("There was an error adding "+player+" to campaign.")
                else:
                    try:
                        queries.addPlayerToCamp(conn,playerID['uid'],cid)
                    except:
                        flash("There was an error adding "+player+" to campaign.")
            
            flash("Successfully edited players")
            return redirect(url_for("campPage"))
        
    else:
        flash("There was an error accessing requested page.")
        return redirect(url_for('home'))

@app.route('/campaign/', methods=["GET","POST"])
def campPage():
    '''Route to the campaing currently stored in the session'''
    id = session['uid']
    conn = pb_view.getConn('pbmod')
    #get all items that the current user can view in this campaign
    all_items = pb_view.get_all(id, session["camp"], conn)
    #ge the campaign name
    name = pb_view.camp_name(session["camp"], conn)
    #load the initial campaign page
    isDM = queries.userIsDM(conn,id,session["camp"])
    if request.method == 'GET':
        return render_template('camp_page.html',  campName=name, comps=all_items, isDM=isDM)
    #if the user clicked a submit button
    else: 
        #if user clicked the "give permission" button
        if request.form["submit"]=="giveperm":
            #get the info on the item giving permission for, including changes 
            #to permissions
            kind = request.form.get("key")
            cid = request.form.get("cid")
            nm = request.form.get("nam")
            selected_users = request.form.getlist("plays")
            #change list of selected user nums to ints so they can go into the 
            #database
            for i in range(len(selected_users)):
                selected_users[i] = int(selected_users[i])
            #get a list of all users in the campagin 
            all_users = pb_view.all_users(id, conn)
            no_perm = []
            #if user in campaign was not checked, revoke permission
            for i in all_users:
                if i not in selected_users:
                    no_perm.append(i)
            #change permissions
            pb_view.change_perms(cid, selected_users, no_perm, id, kind.lower(), conn)
            #get new item list
            all_items_new = pb_view.get_all(id, session["camp"], conn)
            #flash success and relaod page
            #TO BE IMPLEMENTED WITH AJAX FOR FINAL VERSION
            flash("The permissions on the " + kind + " " + nm + " have been updated.")
            return render_template('camp_page.html',  campName=name, comps=all_items_new, isDM=isDM)
        #if user selected to update an item
        else:
            #get info on the item they are updating
            kind = request.form.get("key")
            cid = request.form.get("cid")
            #redirect to update page
            return redirect(url_for('updateItem', cid=cid, key=kind))
            
@app.route('/addType/', methods=["GET","POST"])
def newType():
    '''Route to add new item types to the campaign.'''
    conn = pb_view.getConn('pbmod')
    if request.method == "GET":
        return render_template('new_type.html')
    #if submitting form
    else: 
        #get campaign id and add the new type to the campaign
        campid = session["camp"]
        new_type = request.form.get("kind")
        add = pb_view.add_type(new_type, campid, conn)
        if add==True:
            flash("Type " + new_type + " added")
            return redirect(url_for('campPage'))
        #If it already exists, let user know
        else: 
            flash("Type already exists. Pick a new name.")
            return render_template('new_type.html')

@app.route('/update/<key>/<cid>', methods=['POST', 'GET'])
@app.route('/update/', methods=['POST', 'GET'])
def updateItem(key, cid):
    if request.method == "GET":
        conn = pb_view.getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        if key == "character":
            updateCharacter(cid)
            return redirect(url_for('updateItem', key = "character", cid = cid))
        if key == "towns":
            updateTown(cid)
            return redirect(url_for('updateItem', key = "town", cid = cid))
        if key == "notes":
            updateNote(cid)
            return redirect(url_for('updateItem', key = "notes", cid = cid))
    
            
       
        


def updateCharacter(cid):  # use optional arg 
    
    if request.method == "GET":
        conn = pb_view.getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('''select * from `character` where cid = %s''', [cid])
        results = curs.fetchone
        return render_template('characterform.html', character = results)
    else: 
        submit = request.form.get('submit')
        conn = getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        if submit == 'delete':
            curs.execute('''delete from `character` where cid = %s''', [cid])
            return redirect(url_for('campaign'))
        elif submit=='update':
            name = request.form.get('character-name')
            cclass = request.form.get('cclass')
            race = request.form.get('race')
            alignment = request.form.get('alignment')
            curs.execute('''update `characters` set name = %s, class = %s, race = %s, alignment = %s where cid = %s''', [name, cclass, race, alignment, cid])
            return redirect(url_for('updateItem', tid=tid))
            
    


def updateTown(tid):  # use optional arg 
    if request.method == "GET":
        conn = pb_view.getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('''select * from towns where tid = %s''', [tid])
        results = curs.fetchone()
        return render_template('townsform.html', towns = results)
    else: 
        submit = request.form.get('submit')
        conn = pb_view.getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        if submit == 'delete':
            curs.execute('''delete from towns where tid = %s''', [tid])
            return redirect(url_for('campaign'))
        elif submit=='update':
            name = request.form.get('town-name')
            descrip = request.form.get('towndescr')
            map = request.form.get('townmap')
            curs.execute('''update towns set name = %s, descrip = %s, map = %s where tid = %s''', [name, descrip, map, tid])
            return redirect(url_for('updateTown', tid=tid))    

@app.route('/updatenote/<nid>', methods=['POST', 'GET'])
@app.route('/updatenote/', methods=['POST', 'GET'])
def updateNote(nid):  # use optional arg     
    if request.method == "GET":
        conn = pb_view.getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('''select * from notes where nid = %s''', [nid])
        results = curs.fetchone()
        return render_template('notesform.html', notes = results)
    else: 
        submit = request.form.get('submit')
        conn = getConn('pbmod')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        if submit == 'delete':
            curs.execute('''delete from notes where nid = %s''', [nid])
            return redirect(url_for('campaign'))
        elif submit=='update':
            name = request.form.get('Note-name')
            body = request.form.get('nbody') 
           
            curs.execute('''update notes set name = %s, body = %s, where nid = %s''', [name, body, nid])
            return redirect(url_for('updateNote', nid=nid))
            
        
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8082)

    