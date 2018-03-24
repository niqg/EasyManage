from flask import Flask, json, jsonify, request, session
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

def clearSession():
    session.pop('user', None)
    session.pop('org', None)

#@application.route("/")
#@application.route("/home")

@application.route("/login")
def login():
    if 'user' in session:
        return jsonify(
            key=ERROR_KEY,
            message='A user is already logged in'
        )
    if not ('google_client_id' in request.args):
        return jsonify(
            key=ERROR_KEY,
            message='An ID must be passed'
        )
    cur = mysql.get_db().cursor()
    data = (request.args['google_client_id'],)
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
        command.append("SELECT user.user_id, organization.organization_id FROM user ")
        command.append("INNER JOIN organization ON user.user_id = organization.user_id ")
        command.append("WHERE google_client_id='%s'" % data)
        cur.execute(''.join(command))
        fetched = cur.fetchone()
        session['user'] = fetched[0]
        session['org'] = fetched[1]
    elif(tag == 'EMP'):
        command = []
        command.append("SELECT user.user_id, employee.organization_id FROM ((user ")
        command.append("INNER JOIN employee_user ON user.user_id = employee_user.user_id) ")
        command.append("INNER JOIN employee ON employee_user.employee_id = employee.employee_id) ")
        command.append("WHERE google_client_id='%s'" % data)
        cur.execute(''.join(command))
        fetched = cur.fetchone()
        session['user'] = fetched[0]
        session['org'] = fetched[1]
    elif(tag == 'CON'):
        command = []
        command.append("SELECT user_id FROM user ")
        command.append("WHERE google_client_id='%s'" % data)
        cur.execute(''.join(command))
        session['user'] = cur.fetchone()[0]
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        user_type=tag,
        user_id=session['user']
    )

@application.route("/logout")
def logout():
    if not ('user' in session):
        return jsonify(
            key=WARNING_KEY,
            message='No user was logged in'
        )
    userID = session['user']
    clearSession()
    return jsonify(
        key=SUCCESS_KEY,
        last_user_id=userID
    )

@application.route("/entries",methods=['GET'])
def getAllEntries():
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
            key=WARRNING_KEY,
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
    argsPresent = ['employee_id', 'organization_id']
    valuesPresent = [str(session['user']), str(session['org'])]
    if (request.args.get('title', None) != None):
        argsPresent.append("title")
        valuesPresent.append(''.join(["'", request.args['title'], "'"]))
    if (request.args.get('date_created', None) != None):
        argsPresent.append("date_created")
        valuesPresent.append(''.join(["'", request.args['date_created'], "'"]))
    if (request.args.get('description', None) != None):
        argsPresent.append("description")
        valuesPresent.append(''.join(["'", request.args['description'], "'"]))
    entryType = None
    if (request.args.get('d_type', None) != None):
        argsPresent.append("d_type")
        valuesPresent.append(''.join(["'", request.args['entry_type'], "'"]))
        entryType = request.args['entry_type']
    cur = mysql.get_db().cursor()
    command = []
    command.append("INSERT INTO entry (%s) " % (', '.join(argsPresent),))
    command.append("VALUES (%s)" % (', '.join(valuesPresent),))
    cur.execute(''.join(command))
    entryID = cur.lastrowid
    if(entryType == 'WRK'):
        argsPresent = ['entry_id']
        valuesPresent = [str(entryID)]
        if (request.args.get('status', None) != None):
            argsPresent.append("status")
            valuesPresent.append(''.join(["'", request.args['status'], "'"]))
        if (request.args.get('completion_date', None) != None):
            argsPresent.append("completion_date")
            valuesPresent.append(''.join(["'", request.args['completion_date'], "'"]))
        command = []
        command.append("INSERT INTO work_order (%s) " % (', '.join(argsPresent),))
        command.append("VALUES (%s)" % (', '.join(valuesPresent),))
        cur.execute(''.join(command))
    if(entryType == 'PRC'):
        argsPresent = ['entry_id']
        valuesPresent = [str(entryID)]
        if (request.args.get('status', None) != None):
            argsPresent.append("status")
            valuesPresent.append(''.join(["'", request.args['status'], "'"]))
        if (request.args.get('purchase_ordercol', None) != None):
            argsPresent.append("purchase_ordercol")
            valuesPresent.append(''.join(["'", request.args['purchase_ordercol'], "'"]))
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
            key=WARRNING_KEY,
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
            key=WARRNING_KEY,
            data=[],
            message='No purchase orders were found'
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

@application.route("/entries/<entryID>",methods=['GET'])
def showOneEntry(entryID):
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
    tag = result[1]
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

@application.route("/entries/<entryID>/modify",methods=['PUT'])
def modifyEntry(entryID):
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
    if(tag == 'WRK'):
        execute = False
        command = []
        command.append("UPDATE work_order SET ")
        if 'status' in request.args:
            if request.args['status'] != 'NULL':
                command.append("status = '%s' " % (request.args['status'],))
            else:
                command.append("status = NULL ")
            execute = True
        if 'completion_date' in request.args:
            if request.args['completion_date'] != 'NULL':
                command.append("completion_date = '%s' " % (request.args['completion_date'],))
            else:
                command.append("completion_date = NULL ")
            execute = True
        if execute:
            command.append("WHERE entry_id=%s" % entryID)
            cur.execute(''.join(command))
    elif(tag == 'PRC'):
        execute = False
        command = []
        command.append("UPDATE purchase_order SET ")
        if 'status' in request.args:
            if request.args['status'] != 'NULL':
                command.append("status = '%s' " % (request.args['status'],))
            else:
                command.append("status = NULL ")
            execute = True
        if 'purchase_ordercol' in request.args:
            if request.args['status'] != 'NULL':
                command.append("purchase_ordercol = '%s' " % (request.args['purchase_ordercol'],))
            else:
                command.append("purchase_ordercol = NULL ")
            execute = True
        if execute:
            command.append("WHERE entry_id=%s" % entryID)
            cur.execute(''.join(command))
    execute = False
    command = []
    command.append("UPDATE entry SET ")
    if 'title' in request.args:
        if request.args['title'] != 'NULL':
                command.append("title = '%s' " % (request.args['title'],))
            else:
                command.append("title = NULL ")
        execute = True
    if 'date_created' in request.args:
        if request.args['date_created'] != 'NULL':
                command.append("date_created = '%s' " % (request.args['date_created'],))
            else:
                command.append("date_created = NULL ")
        execute = True
    if 'description' in request.args:
        if request.args['description'] != 'NULL':
                command.append("description = '%s' " % (request.args['description'],))
            else:
                command.append("description = NULL ")
        execute = True
    if execute:
        command.append("WHERE entry_id=%s" % entryID)
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        entry_edited=entryID
    )

@application.route("/entries/<entryID>/remove",methods=['DELETE'])
def removeEntry(entryID):
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

#@application.route("/contacts",methods=['GET'])

#@application.route("/contacts/new",methods=['POST'])

#@application.route("/contacts/search?=<filter>",methods=['GET'])

#@application.route("/contacts/supplier",methods=['GET'])

#@application.route("/contacts/supplier/search?=<filter>",methods=['GET'])

#@application.route("/contacts/contractor",methods=['GET'])

#@application.route("/contacts/contractor/search?=<filter>",methods=['GET'])

#@application.route("/contacts/<contactID>",methods=['GET'])

#@application.route("/contacts/<contactID>/modify",methods=['PUT'])

#@application.route("/contacts/<contactID>/remove",methods=['DELETE'])

#@application.route("/contacts/<contactID>/personnel",methods=['GET']) #Should only work if contactID is a company

#@application.route("/contacts/<contactID>/personnel/search?=<filter>",methods=['GET'])

#@application.route("/about")

#@application.route("/about/axolDev")

#@application.route("/about/ezManage")

#@application.route("/help",methods=['GET'])

#@application.route("/help/search?=<filter>",methods=['GET'])

#@application.route("/help/<tutorialID>",methods=['GET'])

#@application.route("/account",methods=['GET'])

#@application.route("/account/settings",mentods=['GET'])

#@application.route("/account/settings/modify",methods=['PUT'])

#@application.route("/account/personnel",methods=['GET']) #Should only work for organization accounts

#@application.route("/account/personnel/new",methods=['POST'])

#@application.route("/account/personnel/search?=<filter>",methods=['GET'])

#@application.route("/account/personnel/<employeeID>",methods=['GET'])

#@application.route("/account/personnel/<employeeID>/modify",methods=['PUT'])

#@application.route("/account/personnel/<employeeID>/remove",methods=['DELETE'])

#@application.route("/account/personnel/<employeeID>/permissions",methods=['GET']) #Should only work if employeeID is an employee user

#@application.route("/account/personnel/<employeeID>/permissions/modify",methods=['PUT'])

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=5000)
