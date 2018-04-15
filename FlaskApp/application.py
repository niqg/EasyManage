from flask import Flask, json, jsonify, request, session, render_template, redirect
from flaskext.mysql import MySQL

SUCCESS_KEY = 0
ERROR_KEY = 1
WARNING_KEY = 2

application = Flask(__name__)
mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'axolotl'
application.config['MYSQL_DATABASE_DB'] = 'EasyManage'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(application)
application.secret_key = '8X2g= k9Q-2hsT6*M4#sT/f2!'
#session = {} #For cookieless testing

#Permissions Bits
ENTRY_READ = 0
ENTRY_WRITE = 1
ENTRY_REMOVE = 2
CONTACT_READ = 3
CONTACT_WRITE = 4
CONTACT_REMOVE = 5
PERSONNEL_READ = 6
PERSONNEL_WRITE = 7
PERSONNEL_REMOVE = 8
PERMISSION_WRITE = 9
USER_ADD = 10
FULL_PERMISSIONS = 0b11111111111

def checkPermission(userPerm, permLevel):
    return (userPerm >> permLevel) % 2
 
def addPermission(userPerm, permLevel):
    if checkPermission(userPerm, permLevel):
        return userPerm
    return userPerm + (1 << permLevel)

def removePermission(userPerm, permLevel):
    if not checkPermission(userPerm, permLevel):
        return userPerm
    return userPerm - (1 << permLevel)

def clearSession():
    session.pop('user', None)
    session.pop('org', None)
    session.pop('perm', None)
    
#returns the organization based upon a given email
def getOrganization(email):
    print email
    cur = mysql.get_db().cursor()
    
    command = []
    command.append("SELECT organization_id FROM user ")
    command.append("JOIN employee_user using(user_id) ")
    command.append("JOIN employee using(employee_id) ")
    command.append("WHERE username = '%s';" % (email,))
    
    cur.execute(''.join(command))
    
    theOrgId = cur.fetchone()
    cur.close()
    return theOrgId

#checks to see if user exists
#if they do, return the user id, 
#if not, return none
def checkToSeeIfUserExists(username):
    cur = mysql.get_db().cursor()

    command = []
    command.append("SELECT user_id FROM user ")
    command.append("WHERE google_client_id='%s'" % (username,))

    cur.execute(''.join(command))

    #returns the user id or None if not in table. None interpreted as false, userid interpreted as true
    #if needed.
    theUserId = cur.fetchone()
    cur.close()
    return theUserId

@application.route("/",methods=['GET'])
@application.route("/home",methods=['GET'])
def home():
    if 'user' in session:
        return render_template('userPage.html')
    else:
        return redirect("/index")
        
@application.route("/index",methods=['GET'])
def index():
    if not 'user' in session:
        return render_template('index.html')
    else:
        return redirect("/home")

@application.route("/login",methods=['POST'])
def login():
    if 'user' in session:
        return jsonify(
            key=ERROR_KEY,
            message='A user is already logged in'
        )
    if not ('google_client_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='An ID must be passed'
        )
    cur = mysql.get_db().cursor()
    data = (request.form['google_client_id'],)
    command = []
    command.append("SELECT d_type FROM user ")
    command.append("WHERE google_client_id='%s'" % data)
    cur.execute(''.join(command))
    fetched = cur.fetchone()
    if not fetched:
        return jsonify(
            key=WARNING_KEY,
            message='User not found'
        )
    tag = fetched[0]
    if(tag == 'ORG'):
        command = []
        command.append("SELECT user.user_id, user.access, organization.organization_id FROM user ")
        command.append("INNER JOIN organization ON user.user_id = organization.user_id ")
        command.append("WHERE google_client_id='%s'" % data)
        cur.execute(''.join(command))
        fetched = cur.fetchone()
        session['user'] = fetched[0]
        session['perm'] = fetched[1]
        session['org'] = fetched[2]
    elif(tag == 'EMP'):
        command = []
        command.append("SELECT user.user_id, user.access, employee.organization_id FROM ((user ")
        command.append("INNER JOIN employee_user ON user.user_id = employee_user.user_id) ")
        command.append("INNER JOIN employee ON employee_user.employee_id = employee.employee_id) ")
        command.append("WHERE google_client_id='%s'" % data)
        cur.execute(''.join(command))
        fetched = cur.fetchone()
        session['user'] = fetched[0]
        session['perm'] = fetched[1]
        session['org'] = fetched[2]
    elif(tag == 'CON'):
        command = []
        command.append("SELECT user_id, access FROM user ")
        command.append("WHERE google_client_id='%s'" % data)
        cur.execute(''.join(command))
        fetched = cur.fetchone()
        session['user'] = fetched[0]
        session['perm'] = fetched[1]
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
    )

@application.route("/logout")
def logout():
    session.clear()
    return jsonify(
        key=SUCCESS_KEY,
    )

@application.route("/entries",methods=['GET'])
def getAllEntries():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message=['No user is logged in']
        )
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT entry_id, title, date_created, description, d_type FROM entry ")
    command.append("WHERE organization_id=%s" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No entries were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/entries/new",methods=['POST'])
def addNewEntry():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
       )
    if not checkPermission(session['perm'], ENTRY_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    argsPresent = ['employee_id', 'organization_id']
    valuesPresent = [str(session['user']), str(session['org'])]
    if (request.form.get('title', 'NULL') != 'NULL'):
        argsPresent.append("title")
        valuesPresent.append(''.join(["'", request.form['title'], "'"]))
    if (request.form.get('date_created', 'NULL') != 'NULL'):
        argsPresent.append("date_created")
        valuesPresent.append(''.join(["'", request.form['date_created'], "'"]))
    if (request.form.get('description', 'NULL') != 'NULL'):
        argsPresent.append("description")
        valuesPresent.append(''.join(["'", request.form['description'], "'"]))
    entryType = None
    if (request.form.get('entry_type', 'NULL') != 'NULL'):
        argsPresent.append("d_type")
        valuesPresent.append(''.join(["'", request.form['entry_type'], "'"]))
        entryType = request.form['entry_type']
    cur = mysql.get_db().cursor()
    command = []
    command.append("INSERT INTO entry (%s) " % (', '.join(argsPresent),))
    command.append("VALUES (%s)" % (', '.join(valuesPresent),))
    cur.execute(''.join(command))
    entryID = cur.lastrowid
    if(entryType == 'WRK'):
        argsPresent = ['entry_id']
        valuesPresent = [str(entryID)]
        if (request.form.get('status', 'NULL') != 'NULL'):
            argsPresent.append("status")
            valuesPresent.append(''.join(["'", request.form['status'], "'"]))
        if (request.form.get('completion_date', 'NULL') != 'NULL'):
            argsPresent.append("completion_date")
            valuesPresent.append(''.join(["'", request.form['completion_date'], "'"]))
        command = []
        command.append("INSERT INTO work_order (%s) " % (', '.join(argsPresent),))
        command.append("VALUES (%s)" % (', '.join(valuesPresent),))
        cur.execute(''.join(command))
    if(entryType == 'PRC'):
        argsPresent = ['entry_id']
        valuesPresent = [str(entryID)]
        if (request.form.get('status', 'NULL') != 'NULL'):
            argsPresent.append("status")
            valuesPresent.append(''.join(["'", request.form['status'], "'"]))
        if (request.form.get('purchase_ordercol', 'NULL') != 'NULL'):
            argsPresent.append("purchase_ordercol")
            valuesPresent.append(''.join(["'", request.form['purchase_ordercol'], "'"]))
        command = []
        command.append("INSERT INTO purchase_order (%s) " % (', '.join(argsPresent),))
        command.append("VALUES (%s)" % (', '.join(valuesPresent),))
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        new_entry_id=entryID
    )

@application.route("/entries/general",methods=['GET'])
def getAllGenericEntries():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT entry_id, title, date_created, description FROM entry ")
    command.append("WHERE organization_id=%s AND d_type is NULL" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND entry.title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No generic entries were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/entries/work",methods=['GET'])
def getAllWorkOrders():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT entry.entry_id, entry.title, entry.date_created, entry.description, work_order.status, work_order.completion_date FROM entry ")
    command.append("INNER JOIN work_order ON entry.entry_id = work_order.entry_id ")
    command.append("WHERE entry.organization_id=%s AND entry.d_type='WRK'" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND entry.title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No work orders were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/entries/purchase",methods=['GET'])
def getAllPurchaseOrders():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT entry.entry_id, entry.title, entry.date_created, entry.description, purchase_order.status, purchase_order.purchase_ordercol FROM entry ")
    command.append("INNER JOIN purchase_order ON entry.entry_id = purchase_order.entry_id ")
    command.append("WHERE entry.organization_id=%s AND entry.d_type='PRC'" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND entry.title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No purchase orders were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/entries/view",methods=['GET'])
def showOneEntry():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not ('entry_id' in request.args):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    entryID = request.args['entry_id']
    if not entryID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given entry_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], entryID)
    command = []
    command.append("SELECT d_type FROM entry ")
    command.append("WHERE organization_id=%s AND entry_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    tag = result[0]
    data = (entryID,)
    command = []
    if(tag == 'WRK'):
        command.append("SELECT entry.entry_id, entry.title, entry.date_created, entry.description, work_order.status, work_order.completion_date FROM entry ")
        command.append("INNER JOIN work_order ON entry.entry_id = work_order.entry_id ")
        command.append("WHERE entry.entry_id=%s" % data)
    elif(tag == 'PRC'):
        command.append("SELECT entry.entry_id, entry.title, entry.date_created, entry.description, purchase_order.status, purchase_order.purchase_ordercol FROM entry ")
        command.append("INNER JOIN purchase_order ON entry.entry_id = purchase_order.entry_id ")
        command.append("WHERE entry.entry_id=%s" % data)
    else:
        command.append("SELECT entry_id, title, date_created, description FROM entry ")
        command.append("WHERE entry.entry_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/entries/modify",methods=['PUT'])
def modifyEntry():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not ('entry_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    entryID = request.form['entry_id']
    if not entryID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id was not a valid positive integer"
        )
    if not checkPermission(session['perm'], ENTRY_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], entryID)
    command = []
    command.append("SELECT d_type FROM entry ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE organization_id=%s AND entry_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    tag = result[0]
    if(tag == 'WRK'):
        command = []
        columns = []
        command.append("UPDATE work_order SET ")
        if 'status' in request.form:
            if request.form['status'] != 'NULL':
                columns.append("status = '%s'" % (request.form['status'],))
            else:
                columns.append("status = NULL")
        if 'completion_date' in request.form:
            if request.form['completion_date'] != 'NULL':
                columns.append("completion_date = '%s'" % (request.form['completion_date'],))
            else:
                columns.append("completion_date = NULL")
        if columns:
            command.append(', '.join(columns))
            command.append(" WHERE entry_id=%s" % entryID)
            cur.execute(''.join(command))
    elif(tag == 'PRC'):
        command = []
        columns = []
        command.append("UPDATE purchase_order SET ")
        if 'status' in request.form:
            if request.form['status'] != 'NULL':
                columns.append("status = '%s'" % (request.form['status'],))
            else:
                columns.append("status = NULL")
        if 'purchase_ordercol' in request.form:
            if request.form['purchase_ordercol'] != 'NULL':
                columns.append("purchase_ordercol = '%s'" % (request.form['purchase_ordercol'],))
            else:
                columns.append("purchase_ordercol = NULL")
        if columns:
            command.append(', '.join(columns))
            command.append(" WHERE entry_id=%s" % entryID)
            cur.execute(''.join(command))
    command = []
    columns = []
    command.append("UPDATE entry SET ")
    if 'title' in request.form:
        if request.form['title'] != 'NULL':
            columns.append("title = '%s'" % (request.form['title'],))
        else:
            columns.append("title = NULL")
    if 'date_created' in request.form:
        if request.form['date_created'] != 'NULL':
            columns.append("date_created = '%s'" % (request.form['date_created'],))
        else:
            columns.append("date_created = NULL")
    if 'description' in request.form:
        if request.form['description'] != 'NULL':
            columns.append("description = '%s'" % (request.form['description'],))
        else:
            columns.append("description = NULL")
    if columns:
        command.append(', '.join(columns))
        command.append(" WHERE entry_id=%s" % entryID)
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        entry_edited=entryID
    )

@application.route("/entries/remove",methods=['DELETE'])
def removeEntry():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not ('entry_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    entryID = request.form['entry_id']
    if not entryID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id was not a valid positive integer"
        )
    if not checkPermission(session['perm'], ENTRY_REMOVE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], entryID)
    command = []
    command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE organization_id=%s AND entry_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    tag = result[1]
    data = (entryID,)
    if(tag == 'WRK'):
        command = []
        command.append("DELETE FROM work_order ")
        command.append("WHERE entry_id=%s" % data)
        cur.execute(''.join(command))
    elif(tag == 'PRC'):
        command = []
        command.append("DELETE FROM purchase_order ")
        command.append("WHERE entry_id=%s" % data)
        cur.execute(''.join(command))
    command = []
    command.append("DELETE FROM entry ")
    command.append("WHERE entry_id=%s" % data)
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        removed_entry_id=entryID
    )

#@application.route("/testing",methods=['GET'])
#def testing():
#    html_file = open("userPage.html")
#    html = html_file.read()
#    html_file.close()
#    return html

#@application.route("/testingJSgetEntries",methods=['GET'])
#def testingJSgetEntries():
#    js_file = open(r"./static/js/getEntries.js").read()
#    js = js_file.read()
#    js_file.close()
#    return js

#@application.route("/testingCalendar", methods=['GET'])
#def testingCalendar():
#    html_file = open("quickstart.html")
#    html = html_file.read()
#    html_file.close()
#    return html

@application.route("/contacts",methods=['GET'])
def getContacts():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
    )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], CONTACT_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT name, company_name, d_type FROM contact ")
    command.append("WHERE organization_id=%s" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No contacts were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

#@application.route("/testingSignUpPage.html")
#def signUpPage():
#    html = open("/var/www/html/signUpPage.html")
#    html_text = html.read()
#    html.close()
#    return html_text

@application.route("/contacts/new",methods=['POST'])
def addNewContact():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
       )
    if not checkPermission(session['perm'], CONTACT_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    argsPresent = ['organization_id']
    valuesPresent = [str(session['org'])]
    if (request.form.get('name', 'NULL') != 'NULL'):
        argsPresent.append("name")
        valuesPresent.append(''.join(["'", request.form['name'], "'"]))
    if (request.form.get('company_name', 'NULL') != 'NULL'):
        argsPresent.append("company_name")
        valuesPresent.append(''.join(["'", request.form['company_name'], "'"]))
    contactType = None
    if (request.form.get('contact_type', 'NULL') != 'NULL'):
        argsPresent.append("d_type")
        valuesPresent.append(''.join(["'", request.form['contact_type'], "'"]))
        contactType = request.form['contact_type']
    cur = mysql.get_db().cursor()
    command = []
    command.append("INSERT INTO contact (%s) " % (', '.join(argsPresent),))
    command.append("VALUES (%s)" % (', '.join(valuesPresent),))
    cur.execute(''.join(command))
    contactID = cur.lastrowid
    if(contactType == 'SPP'):
        command = []
        command.append("INSERT INTO supplier (contact_id) ")
        command.append("VALUES (%s)" % (contactID,))
        cur.execute(''.join(command))
    if(contactType == 'CNT'):
        command = []
        command.append("INSERT INTO contractor (contact_id) ")
        command.append("VALUES (%s)" % (contactID,))
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        new_contact_id=contactID
    )

@application.route("/contacts/supplier",methods=['GET'])
def getAllSupliers():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], CONTACT_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT name, company_name FROM contact ")
    command.append("WHERE organization_id=%s AND d_type='SPP'" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND entry.title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No supliers were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/contacts/contractor",methods=['GET'])
def getAllContractors():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], CONTACT_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT name, company_name FROM contact ")
    command.append("WHERE organization_id=%s AND d_type='CNT'" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND entry.title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No contractors were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/contacts/view",methods=['GET'])
def showOneContact():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not ('contact_id' in request.args):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    contactID = request.args['contact_id']
    if not contactID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given entry_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], CONTACT_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], contactID)
    command = []
    command.append("SELECT name, company_name FROM contact ")
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    result = {info : cur.fetchone()}
    if not result['info']:
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    data = (contactID,)
    command = []
    command.append("SELECT email.email, contact_email.priority FROM email ")
    command.append("INNER JOIN contact_email ON email.email_id = contact_email.email_id ")
    command.append("WHERE contact_email.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['email'] = cur.fetchall()
    command = []
    command.append("SELECT phone_number.phone_number, phone_number.type, contact_phone_number.priority FROM phone_number ")
    command.append("INNER JOIN contact_phone_number ON phone_number.phone_number_id = contact_phone_number.phone_number_id ")
    command.append("WHERE contact_phone_number.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['phone'] = cur.fetchall()
    command = []
    command.append("SELECT address.address, address.zipcode, address.city, contact_address.priority FROM address ")
    command.append("INNER JOIN contact_address ON address.address_id = contact_address.address_id ")
    command.append("WHERE contact_address.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['address'] = cur.fetchall()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        info=result['info'],
        emails=result['email'],
        phone_numbers=result['phone'],
        addresses=result['address']
    )

def addPhoneNumber(contactID, phoneNumber, dtype, priority):
    cur = mysql.get_db().cursor()
    
    command = []
    command.append("INSERT INTO phone_number (phone_number, type) ")
    command.append("VALUES (%s, '%s');" % phoneNumber, dtype)
    
    cur.execute(''.join(command))
    
    phoneNumberID = cur.lastrowid
    
    command = []
    command.append("INSERT INTO contact_phone_number (contact_id, phone_number_id, priority) ")
    command.append("VALUES (%s, %s, %s);" % contactID, phoneNumberID, priority)
    
    cur.execute(''.join(command))
    
    mysql.get_db().commit()
    cur.close()
    

def addEmail(contactID, email, priority):
    cur = mysql.get_db().cursor()
    
    command = []
    command.append("INSERT INTO email (email) ")
    command.append("VALUES ('%s');" % email)
    
    cur.execute(''.join(command))
    
    emailID = cur.lastrowid
    
    command = []
    command.append("INSERT INTO contact_email (contact_id, email_id, priority) ")
    command.append("VALUES (%s, %s, %s);" % contactID, emailID, priority)
    
    cur.execute(''.join(command))
    
    mysql.get_db().commit()
    cur.close()

def addAddress(contactID, address, zipcode, city, priority):
    cur = mysql.get_db().cursor()
    
    command = []
    command.append("INSERT INTO address (address, zipcode, city) ")
    command.append("VALUES ('%s', '%s', '%s');" % address, zipcode, city)
    
    cur.execute(''.join(command))
    
    addressID = cur.lastrowid
    
    command = []
    command.append("INSERT INTO contact_address (contact_id, address_id, priority) ")
    command.append("VALUES (%s, %s, %s);" % contactID, addressID, priority)
    
    cur.execute(''.join(command))
    
    mysql.get_db().commit()
    cur.close()


#modifies a contact to give it access points (email, phoneNums, Addresses)
#data from js should be in the form
#emails:{emailString:"", email_priority:"Might be a num or string? Not sure how js works"}
#contactID:contact ID to have stuff added to. 
#phoneNums and addresses are similar to emails. 
@application.route("/contacts/modify/giveAccessPoints",methods=['PUT'])
def modifyContact():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
       )
    if not checkPermission(session['perm'], CONTACT_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    
    contactID = request.form.get("contactID")
    
    emails = request.form.get("emails")      #should return a set of dicts
    phoneNums = request.form.get("phoneNums")#should return a set of dicts
    addresses = request.form.get("addresses")#should return a set of dicts
    
    if(emails is not None):
        for email in emails:
            addEmail(contactID, email.get("emailString"), email.get("email_priority"))
    
    if(phoneNums is not None):
        for phoneNum in phoneNums:
            addPhoneNumber(contactID, phoneNum.get("phoneNumberString"), phoneNum.get("d_type"), phoneNum.get("phone_priority"))
            
    if(addresses is not None):
        for address in addresses:
            addAddress(contactID, address.get("address_string"), address.get("zipcode_string"), address.get("city_string"), address.get("priority_string"))
            
    return jsonify(
        key=SUCCESS_KEY,
        entry_edited=entryID
    )

#@application.route("/contacts/modify/giveAccessPoints",methods=['PUT'])


    
    
#@application.route("/contacts/<contactID>/remove",methods=['DELETE'])

#@application.route("/about")

#@application.route("/about/axolDev")

#@application.route("/about/ezManage")

#@application.route("/help",methods=['GET'])

#@application.route("/help/search?=<filter>",methods=['GET'])

#@application.route("/help/<tutorialID>",methods=['GET'])

@application.route("/account/new",methods=['POST'])
def addNewUser():
    email = request.form.get("userEmail")
    userExists = checkToSeeIfUserExists(email)
    if(userExists):
        return jsonify(
            key=ERROR_KEY,
            message='That user already exists'
        )
    user_type = request.form.get("userType")
    if(user_type == "ORG"):
        access = FULL_PERMISSIONS
    else:
        if not ('user' in session):
            return jsonify(
                key=ERROR_KEY,
                message='No user is logged in'
            )
        if not ('org' in session):
            return jsonify(
                key=ERROR_KEY,
                message='User logged in is not an employee or organization'
            )
        if not checkPermission(session['perm'], USER_ADD):
            return jsonify(
                key=ERROR_KEY,
                message='User does not have the permission'
            )
        access = 0
    cur = mysql.get_db().cursor()
    data = (email, request.form.get('google_client_id'), access, user_type)
    command = []
    command.append("INSERT INTO user (username, google_client_id, access, d_type) ")
    command.append("VALUES('%s', '%s', %s, '%s')" % data)
    cur.execute(''.join(command))
    userID = cur.lastrowid
    if(user_type == "ORG"):
        data = (userID, request.form['org_name'])
        command = []
        command.append("INSERT INTO organization (user_id, organization_name) ")
        command.append("VALUES (%s, '%s')" % data)
        cur.execute(''.join(command))
    elif(user_type == 'EMP'):
#        data = (session['org'], request.form.get('employee_id'))
#        command = []
#        command.append("SELECT employee_id FROM employee ")
#        command.append("WHERE organization_id=%s AND employee_id=%s" % (data))
#        cur.execute(''.join(command))
#        if not cur.fetchone():
#            return jsonify(
#            key=ERROR_KEY,
#            message='Employee either does not exist or does not belong to the organization'
#        )
        data = (session['org'], request.form.get("fName"), request.form.get("lName"), request.form.get("title"))
        command = []
        command.append("INSERT INTO employee (organization_id, first_name, last_name, position) ")
        command.append("VALUES (%s, '%s', '%s', '%s')" % (data))
        cur.execute(''.join(command))
        employee_id = cur.lastrowid
        data = (userID, employee_id)
        command = []
        command.append("INSERT INTO employee_user (user_id, employee_id) ")
        command.append("VALUES (%s, %s)" % data)
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        message='User Successfully added to the database')

@application.route("/account/personnel",methods=['GET'])
def getAllEmployees():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], PERSONNEL_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT first_name, last_name, postiion FROM employee ")
    command.append("WHERE organization_id=%s" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND title LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No employees were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/account/personnel/new",methods=['POST'])
def addEmployee():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    print "here"
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], PERSONNEL_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    data = (session['org'], request.form.get("fName"), request.form.get("lName"), request.form.get("title"))
    command = []
    command.append("INSERT INTO employee (organization_id, first_name, last_name, position) ")
    command.append("VALUES (%s, '%s', '%s', '%s')" % (data))
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/account/personnel/view",methods=['GET'])
def showOneEmployee():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not ('employee_id' in request.args):
        return jsonify(
            key=ERROR_KEY,
            message='No employee_id given'
        )
    employee_id = request.args['employee_id']
    if not employee_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given employee_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], PERSONNEL_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], employee_id)
    command = []
    command.append("SELECT first_name, last_name, position FROM employee ")
    command.append("WHERE organization_id=%s AND employee_id=%s" % data)
    cur.execute(''.join(command))
    result = {info : cur.fetchone()}
    if not result['info']:
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    data = (employee_id,)
    command = []
    command.append("SELECT email.email, employee_email.priority FROM email ")
    command.append("INNER JOIN employee_email ON email.email_id = employee_email.email_id ")
    command.append("WHERE employee_email.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['email'] = cur.fetchall()
    command = []
    command.append("SELECT phone_number.phone_number, phone_number.type, employee_phone_number.priority FROM phone_number ")
    command.append("INNER JOIN employee_phone_number ON phone_number.phone_number_id = employee_phone_number.phone_number_id ")
    command.append("WHERE employee_phone_number.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['phone'] = cur.fetchall()
    command = []
    command.append("SELECT address.address, address.zipcode, address.city, employee_address.priority FROM address ")
    command.append("INNER JOIN employee_address ON address.address_id = employee_address.address_id ")
    command.append("WHERE employee_address.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['address'] = cur.fetchall()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        info=result['info'],
        emails=result['email'],
        phone_numbers=result['phone'],
        addresses=result['address']
    )

#@application.route("/account/personnel/modify",methods=['PUT'])

#@application.route("/account/personnel/remove",methods=['DELETE'])

@application.route("/account/personnel/permissions",methods=['GET'])
def getAllUserEmployees():
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    if not checkPermission(session['perm'], PERSONNEL_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    command = []
    command.append("SELECT e.first_name, e.last_name, e.position, u.username, u.access  ")
    command.append("FROM employee e ")
    command.append("JOIN employee_user USING (employee_id) ")
    command.append("JOIN user u USING (user_id) ")
    command.append("WHERE ((e.organization_id = %s) " % (session['org'],))
    command.append("AND (u.d_type = 'EMP') ")
    command.append("AND NOT (u.user_id = %s ))" % (session['user'],))#<> is not equal to
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

#@application.route("/account/personnel/permissions/modify",methods=['PUT'])

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=80)
