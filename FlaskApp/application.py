from flask import Flask, json, jsonify, request, session
from flaskext.mysql import MySQL

application = Flask(__name__)
mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'axolotl'
application.config['MYSQL_DATABASE_DB'] = 'EasyManage'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(application)
application.secret_key = '8X2g= k9Q-2hsT6*M4#sT/f2!'

#@application.route("/")

#@application.route("/home")

@application.route("/login")
def main():
    #Should do someting if there is already a user logged in to the session
    cur = mysql.get_db().cursor()
    command = []
    args['gci'] = request.form['GoogleClientID']
    command.append('SELECT d_type FROM user ')
    command.append('WHERE google_client_id=%s')
    data = (args['gci'])
    cur.execute(''.join(command), data)
    fetched = cur.fetchone()[0]
    if(fetched == 'ORG'):
       loginOrganization(args['gci']) 
    elif(fetched == 'EMP'):
        loginEmployee(args['gci'])
    elif(fetched == 'CON'):
        loginContact(args['gci'])
    cur.close()

def loginOrganization(GoogleClientID):
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT user.user_id, organization.organization_id FROM user ')
    command.append('INNER JOIN organization ON user.user_id = organization.user_id ')
    command.append('WHERE google_client_id=%s')
    data = (GoogleClientID)
    cur.execute(''.join(command), data)
    fetched = cur.fetchone()
    session['user'] = fetched[0]
    session['org'] = fetched[1]
    cur.close()

def loginEmployee(GoogleClientID):
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT user.user_id, employee.organization_id FROM ((user ')
    command.append('INNER JOIN employee_user ON user.user_id = employee_user.user_id) ')
    command.append('INNER JOIN employee ON employee_user.employee_id = employee.employee_id) ')
    command.append('WHERE google_client_id=%s')
    data = (GoogleClientID)
    cur.execute(''.join(command), data)
    fetched = cur.fetchone()
    session['user'] = fetched[0]
    session['org'] = fetched[1]
    cur.close()

def loginContact(GoogleClientID):
    cur = mysql.get_db().cursor()
    command = []
    command.append('SELECT user_id FROM user ')
    command.append('WHERE google_client_id=%s')
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
    command.append('SELECT title, date_created, description, d_type FROM entry ')
    command.append('WHERE organization_id=%s')
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
    command.append('INSERT INTO entry (employee_id, organization_id, title, date_created, description, d_type) ')
    command.append('VALUES (%s, %s, %s, %s, %s, %s); ')
    command.append('SELECT scope_identity()') #I want to make the commands atomic in the future
    data = (session['user'], session['org'], args['title'], args['date'], args['descp'], args['dType'])
    cur.execute(command, data, True)
    args['entryID'] = cur.fetchone()[0]
    if(args['dType'] == 'WRK'):
        command = []
        args['status'] = request.form['status']
        args['compDate'] = request.form['completionDate']
        command.append('INSERT INTO work_order (entry_id, status, completion_date) ')
        command.append('VALUES (%s, %s, %s)')
        data = (args['entryID'], args['status'], args['compDate'])
        cur.execute(''.join(command), data)
    if(args['dType'] == 'PRC'):
        command = []
        args['status'] = request.form['status']
        command.append('INSERT INTO purchase_order (entry_id, status) ')
        command.append('VAlUES (%s, %s)')
        data = (args['entryID'], args['status'])
        cur.execute(''.join(command), data)
    cur.close()

#@application.route("/entries/search?=<filter>",methods=['GET'])

#@application.route("/entries/work",methods=['GET'])

#@application.route("/entries/work/search?=<filter>",methods=['GET'])

#@application.route("/entries/purchase",methods=['GET'])

#@application.route("/entries/purchase/search?=<filter>",methods=['GET'])

#@application.route("/entries/<entryID>",methods=['GET'])

#@application.route("/entries/<entryID>/modify",methods=['PUT'])

#@application.route("/entries/<entryID>/remove",methods=['DELETE'])

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
    application.run(host=0.0.0.0, port=5000)
