from flask import Flask, json, jsonify, request, session
from flaskext.mysql import MySQL
import ConfigParser

application = Flask(__name__)
mysql = MySQL()
flask_application.config['MYSQL_DATABASE_USER'] = config.get('config','username')
flask_application.config['MYSQL_DATABASE_PASSWORD'] = config.get('config','password')
flask_application.config['MYSQL_DATABASE_DB'] = config.get('config','database')
flask_application.config['MYSQL_DATABASE_HOST'] = config.get('config','hostname')
mysql.init_app(application)
app.secret_key = '8X2g= k9Q-2hsT6*M4#sT/f2!'

@application.route("/")

@application.route("/home")

@application.route("/login")
def main(GoogleClientID):
    #Should do someting if there is already a user logged in to the session
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT DType FROM User ')
    command.append('WHERE GoogleClientID=')
    command.append(GoogleClientID)
    cur.execute(''.join(command))
    fetched = cur.fetchone()[0]
    if(fetched == 'ORG'):
       loginOrganization(GoogleClientID) 
    elif(fetched == 'EMP'):
        loginEmployee(GoogleClientID)
    elif(fetched == 'CON'):
        loginContact(GoogleClientID)
    else:
        #ERROR
    del(fetched)
    cur.fetchall()

def loginOrganization(GoogleClientID):
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT User.UserID, OrganizationAccount.OrgID FROM User ')
    command.append('INNER JOIN OrganizationAccount ON User.UserID = OrganizationAccount.UserID ')
    command.append('WHERE GoogleClientID=(%s)')
    data = (GoogleClientID)
    cur.execute(''.join(command), data)
    fetched = cur.fetchone()
    session['user'] = fetched[0]
    session['org'] = fetched[1]
    cur.close()

def loginEmployee(GoogleClientID):
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT User.UserID, Employee.OrgID FROM ((User ')
    command.append('INNER JOIN EmployeeUser ON User.UserID = EmployeeUser.UserID) ')
    command.append('INNER JOIN Employee ON EmployeeUser.EmployeeID = Employee.EmployeeID) ')
    command.append('WHERE GoogleClientID=(%s)')
    data = (GoogleClientID)
    cur.execute(''.join(command), data)
    fetched = cur.fetchone()
    session['user'] = fetched[0]
    session['org'] = fetched[1]
    cur.close()

def loginContact(GoogleClientID):
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT UserID FROM User ')
    command.append('WHERE GoogleClientID=(%s)')
    data = (GoogleClientID)
    cur.execute(''.join(command), data)
    session['user'] = cur.fetchone()[0]
    session['org'] = None
    cur.close()

@application.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('org', None)

@application.route("/entries",methods=['GET'])
def getAllEntries():
    #If not logged in or not an employee return some error
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT * FROM Entry ')
    command.append('WHERE OrgID=(%s)')
    data = (session['org'])
    cur.execute(''.join(command), data)
    toReturn = cur.fetchall()
    cur.close()
    return jsonify(result=toReturn)

@application.route("/entries/new",methods=['POST'])
def addNewEntry():
    #If not logged in or not an employee return some error
    cur = mysql.get_db().cursor()
    command = []
    args['title'] = request.form['title']
    args['date'] = request.form['date']
    args['descp'] = request.form['description']
    args['dType'] = request.form['entryType']
    command.append('INSERT INTO Entry (CreatedByEmployeeID, OrgID, Title, DateCreated, Description, DType) ')
    command.append('VALUES (%s, %s, %s, %s, %s, %s); ')
    command.append('SELECT scope_identity()') #I want to make the commands atomic in the future
    data = (session['user'], session['org'], args['title'], args['date'], args['descp'], args['dType'])
    cur.execute(command, data, True)
    args['entryID'] = cur.fetchone()[0]
    if(args['dType'] == 'WRK'):
        command = []
        args['status'] = request.form['status']
        args['compDate'] = request.form['completionDate']
        command.append('INSERT INTO WorkOrder (EntryID, Status, CompletionDate) ')
        command.append('Values (%s, %s, %s)')
        data = (args['entryID'], args['status'], args['compDate'])
        cur.execute(''.join(command), data)
    if(args['dType'] == 'PRC'):
        command = []
        args['status'] = request.form['status']
        command.append('INSERT INTO WorkOrder (EntryID, Status) ')
        command.append('Values (%s, %s)')
        data = (args['entryID'], args['status'])
        cur.execute(''.join(command), data)
    cur.close()

@application.route("/entries/search?=<filter>",methods=['GET'])

@application.route("/entries/work",methods=['GET'])

@application.route("/entries/work/search?=<filter>",methods=['GET'])

@application.route("/entries/purchase",methods=['GET'])

@application.route("/entries/purchase/search?=<filter>",methods=['GET'])

@application.route("/entries/<entryID>",methods=['GET'])

@application.route("/entries/<entryID>/modify",methods=['PUT'])

@application.route("/entries/<entryID>/remove",methods=['DELETE'])

@application.route("/contacts",methods=['GET'])

@application.route("/contacts/new",methods=['POST'])

@application.route("/contacts/search?=<filter>",methods=['GET'])

@application.route("/contacts/supplier",methods=['GET'])

@application.route("/contacts/supplier/search?=<filter>",methods=['GET'])

@application.route("/contacts/contractor",methods=['GET'])

@application.route("/contacts/contractor/search?=<filter>",methods=['GET'])

@application.route("/contacts/<contactID>",methods=['GET'])

@application.route("/contacts/<contactID>/modify",methods=['PUT'])

@application.route("/contacts/<contactID>/remove",methods=['DELETE'])

@application.route("/contacts/<contactID>/personnel",methods=['GET']) #Should only work if contactID is a company

@application.route("/contacts/<contactID>/personnel/search?=<filter>",methods=['GET'])

@application.route("/about")

@application.route("/about/axolDev")

@application.route("/about/ezManage")

@application.route("/help",methods=['GET'])

@application.route("/help/search?=<filter>",methods=['GET'])

@application.route("/help/<tutorialID>",methods=['GET'])

@application.route("/account",methods=['GET'])

@application.route("/account/settings",mentods=['GET'])

@application.route("/account/settings/modify",methods=['PUT'])

@application.route("/account/personnel",methods=['GET']) #Should only work for organization accounts

@application.route("/account/personnel/new",methods=['POST'])

@application.route("/account/personnel/search?=<filter>",methods=['GET'])

@application.route("/account/personnel/<employeeID>",methods=['GET'])

@application.route("/account/personnel/<employeeID>/modify",methods=['PUT'])

@application.route("/account/personnel/<employeeID>/remove",methods=['DELETE'])

@application.route("/account/personnel/<employeeID>/permissions",methods=['GET']) #Should only work if employeeID is an employee user

@application.route("/account/personnel/<employeeID>/permissions/modify",methods=['PUT'])
