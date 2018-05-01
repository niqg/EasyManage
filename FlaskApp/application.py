from flask import Flask, json, jsonify, request, session, render_template, redirect, send_file
from flaskext.mysql import MySQL
import os.path
import random
import string

#unused imports for the incomplete cryptosystem: to be finished in future work
#import os
#from cryptography.fernet import Fernet
#from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives import hashes
#from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#status codes for endpoint results
SUCCESS_KEY = 0
ERROR_KEY = 1
WARNING_KEY = 2

application = Flask(__name__)
mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'axolotl'
application.config['MYSQL_DATABASE_DB'] = 'EasyManage'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
application.config['UPLOAD_FOLDER'] = '/var/www/html/files'
application.secret_key = '8X2g= k9Q-2hsT6*M4#sT/f2!'
mysql.init_app(application)
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

#return 1 if the user has permissions at given permlevel (as defined by the permission bits above) and 0 otherwise
def checkPermission(userPerm, permLevel):
    return (userPerm >> permLevel) % 2

#if the user doesn't have permission at the given level, give it to them
def addPermission(userPerm, permLevel):
    if checkPermission(userPerm, permLevel):
        return userPerm
    return userPerm + (1 << permLevel)

#if the user does have permission at the fgiven level, take it away
def removePermission(userPerm, permLevel):
    if not checkPermission(userPerm, permLevel):
        return userPerm
    return userPerm - (1 << permLevel)

#clear the contents of the user-stored session
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

#function used to set up parameters of cryptosystem
#def setupCryptosystem():
#    subpass = getUserName()
#    if subpass.key == 1:
#        return plaintext
#    password = subpass.data[0]
#    salt = str.encode(b"9B9F7701")
#    kdf = PBKDF2HMAC(
#        algorithm=hashes.SHA256(),
#        length=32,
#        iterations=100000,
#        salt=salt,
#        backend=default_backend()
#    )
#    key = base64.urlsafe_b64encode(kdf.derive(password))
#    f = Fernet(key)
#    return f

#Implementation of AES symmetric-key encryption
#def encrypt(plaintext):
#    f = setupCryptosystem()
#    if f == plaintext
#	return plaintext
#    token = f.encrypt(plaintext)
#    return token

#Implementation of AES symmetric-key decryption
#def decrypt(ciphertext):
#    f = setupCryptosystem()
#    if f == ciphertext:
#	return ciphertext
#    token = f.decrypt(str.encode(str(ciphertext)))
#    return token

#map the root of our application (what you see upon initially viewing the page) to the /home page
@application.route("/",methods=['GET'])
@application.route("/home",methods=['GET'])
def home():
    if 'user' in session:
        return render_template('userPage.html')
    else:
        return redirect("/index")

#If there is a user logged in, take them to the home page. Otherwise, redirect to the signin page.
@application.route("/index",methods=['GET'])
def index():
    if not 'user' in session:
        return render_template('index.html')
    else:
        return redirect("/home")

#function to be performed upton user login
@application.route("/login",methods=['POST'])
def login():
    #if a user is already logged in, return an error
    if 'user' in session:
        return jsonify(
            key=ERROR_KEY,
            message='A user is already logged in'
        )
    #if a valid google client id is not available, return an error
    if not ('google_client_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='An ID must be passed'
        )
    #retrieving the type of user attempting to log in from the database
    cur = mysql.get_db().cursor()
    data = (request.form['google_client_id'],)
    command = []
    command.append("SELECT d_type FROM user ")
    command.append("WHERE google_client_id='%s'" % data)
    cur.execute(''.join(command))
    fetched = cur.fetchone()
    #Return a warning if the user is not found in the system
    if not fetched:
        return jsonify(
            key=WARNING_KEY,
            message='User not found'
        )
    tag = fetched[0]
    #store appropriate values from the database in 'session' depending on the type of user
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

#clear 'session' so no user data is stored anymore so there is no currently logged in user anymore
@application.route("/logout")
def logout():
    session.clear()
    return jsonify(
        key=SUCCESS_KEY,
    )

#Endpoint to get all inventory entries
@application.route("/entries",methods=['GET'])
def getAllEntries():
    #if there is no current user logged in, return an error
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message=['No user is logged in']
        )
    #if there is no org affiliated with the logged in user or lack thereof, return an error
    if not ('org' in session):
        return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    #if the user doesn't have permissino to read entries, return an error
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #get the entries from the database and filter them based on the requrest gotten from getFilteredEntries.js
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
    #If no entries matched the query, return an empty array and a warning
    if not result:
        return jsonify(
            key=WARNING_KEY,
            data=[],
            message='No entries were found'
        )
    #if all goes well, return a success code and the entries fetched
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

#endpoint to add a new entry to the system
@application.route("/entries/new",methods=['POST'])
def addNewEntry():
    #Return an error if no user is logged in
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    #Return error if there is no organization/employee logged in
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
       )
    #Return error if the user in the current session does not have permission to create an entry
    if not checkPermission(session['perm'], ENTRY_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #start building a list of the arguments being used to create the entry.
    #If it's made it this far, it must have an employee ID and organization ID associated 
    argsPresent = ['employee_id', 'organization_id']
    valuesPresent = [str(session['user']), str(session['org'])]
    #If a title for the entry was passed, then it is a present arguemtn
    if (request.form.get('title', 'NULL') != 'NULL'):
        argsPresent.append("title")
        valuesPresent.append(''.join(["'", request.form['title'], "'"]))
    #If a date created is passed in, add it
    if (request.form.get('date_created', 'NULL') != 'NULL'):
        argsPresent.append("date_created")
        valuesPresent.append(''.join(["'", request.form['date_created'], "'"]))
    #If a description is passed in, add it 
    if (request.form.get('description', 'NULL') != 'NULL'):
        argsPresent.append("description")
        valuesPresent.append(''.join(["'", request.form['description'], "'"]))
    #Default the entry to not have a type. IF it does have a type, add that to the list of args present
    entryType = None
    if (request.form.get('entry_type', 'NULL') != 'NULL'):
        argsPresent.append("d_type")
        valuesPresent.append(''.join(["'", request.form['entry_type'], "'"]))
        entryType = request.form['entry_type']
    #Use the array arguments passed in to construct a query to create a new entry
    cur = mysql.get_db().cursor()
    command = []
    command.append("INSERT INTO entry (%s) " % (', '.join(argsPresent),))
    command.append("VALUES (%s)" % (', '.join(valuesPresent),))
    cur.execute(''.join(command))
    entryID = cur.lastrowid
    #Work Order is a specific type of entry. So, if the entry is a work order,
    #request from js and add to the entry the fields of status (complete or incomplete) and completion date
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
    #Like work order, purchase order is a specific type of entry. If the entry is a purchase order,
    #Retrieve and add the fields of 'status' and 'purchase_ordercal'
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

#endpoint to get names of and data in pdf files attached to a given entry
@application.route("/entries/pdf",methods=['GET'])
def getPDFNames():
    #if no user is logged in, return error
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    #if no organization is logged in, return error
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    #If there's no id to identify the entry to get pdf's from, return error
    if not ('entry_id' in request.args):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    entry_id = request.args['entry_id']
    #If entry id is not valid, return an error
    if not entry_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id was not a valid positive integer"
        )
    #If the user doesn't have permission to read this entry, return error
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #Construct and executre SQL query to get the pdf attached to the entry
    cur = mysql.get_db().cursor()
    data = (session['org'], entry_id)
    command = []
    command.append("SELECT pdf.pdf_id, pdf.pdf_data FROM pdf ")
    command.append("INNER JOIN entry ON entry.entry_id = pdf.entry_id ")
    command.append("WHERE entry.organization_id=%s AND entry.entry_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

#endpoint to get the aftual data in a PDF file based on it's ID
@application.route("/entries/pdf/view",methods=['GET'])
def viewPDF():
    #if no user is logged in, return error
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    #if no org is logged in, returbn error
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    #if no identifyer for the pdf to get data from, return error
    if not ('pdf_id' in request.args):
        return jsonify(
            key=ERROR_KEY,
            message='No pdf_id given'
        )
    pdf_id = request.args['pdf_id']
    #If pdf identifyer is not valid, return error
    if not pdf_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given pdf_id was not a valid positive integer"
        )
    #IF user doesn't have permsisino to read entries, return error
    if not checkPermission(session['perm'], ENTRY_READ):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #construct and execute query to get pdf data
    cur = mysql.get_db().cursor()
    data = (session['org'], pdf_id)
    command = []
    command.append("SELECT pdf.pdf_data FROM pdf ")
    command.append("INNER JOIN entry ON entry.entry_id = pdf.entry_id ")
    command.append("WHERE entry.organization_id=%s AND pdf.pdf_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given pdf_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    cur.close()
    return send_file(os.path.join(application.config['UPLOAD_FOLDER'], result[0]))

#endpoint to add a pdf to a given entry
@application.route("/entries/pdf/add",methods=['POST'])
def addPDF():
    print "pdf" in request.files
    #return an error if no user is logged in
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    #return error if no organization is logged in
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    #return error if no entry is gfiven to attach PDF to
    if not ('entry_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    entryID = request.form['entry_id']
    #Return error if entry ID is invalid
    if not entryID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id was not a valid positive integer"
        )
    #Retrn error if user don't have permissions
    if not checkPermission(session['perm'], ENTRY_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    pdf = request.files['pdf']
    #If invalid PDF name, do not add it and return error
    if pdf.filename == '':
        return jsonify(
            key=ERROR_KEY,
            message='No file recieved'
        )
    #construct and execute query to add the PDF's id to the entry it is attached to
    cur = mysql.get_db().cursor()
    data = (session['org'], entryID)
    command = []
    command.append("SELECT entry_id FROM entry ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE organization_id=%s AND entry_id=%s" % data)
    cur.execute(''.join(command))
    if not cur.fetchone():
        return jsonify(
            key=ERROR_KEY,
            message="The given entry_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    #Store the actual PDF data in a specified point on the server and save that path on the server to the database
    file_name = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(30)) + '.pdf'
    file_path = os.path.join(application.config['UPLOAD_FOLDER'], file_name)
    while os.path.exists(file_path):
        file_name = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(30)) + '.pdf'
        file_path = os.path.join(application.config['UPLOAD_FOLDER'], file_name)
    data = (entryID, file_name)
    command = []
    command.append("INSERT INTO pdf (entry_id, pdf_data) ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("VALUES (%s, '%s')" % data)
    cur.execute(''.join(command))
    pdf.save(file_path)
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY
    )

#endpoint to get all entries that are neither purchase orders or work orders
@application.route("/entries/general",methods=['GET'])
def getAllGenericEntries():
    #Return an error if there is no user logged in, no organization logged in, or if the user doesn't have permission to get these entries
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
    #construcrt and execute query to get all generic entries with the given filter applied if there is one passed
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
    #Return a warning and an empty array if there are no entries
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

#Endpoint to get all work orders
@application.route("/entries/work",methods=['GET'])
def getAllWorkOrders():
    #return an error if no user is logged in, no organization is logged in, or if the current user doesn't have permission to read these work orders
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
    #Construct and execute query to get the work order and it's related fields if the work order's title matches the filter applied (if any)
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
 #Return a warning and an empty array if there are no entries
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

##ndpoint to get all purchase orders
@application.route("/entries/purchase",methods=['GET'])
def getAllPurchaseOrders():
 #return an error if no user is logged in, no organization is logged in, or if the current user doesn't have permission to read these work orders
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
     #Construct and execute query to get the purchase order and it's related fields if the order's title matches the filter applied (if any)
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
     #Return a warning and an empty array if there are no entries
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

#Endpoint to get a single entry (can be general, work, or purchase order) based on a given entry id
@application.route("/entries/view",methods=['GET'])
def showOneEntry():
     #return an error if no user is logged in, no organization is logged in, or if the current user doesn't have permission to read these work orders
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
    #If the entry id is either not given or not valid, return an error.
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
    #constrtuct and execute the query to get the type of entry so that the right componenets of the entry can be query'd for
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
    #Construct command to grab the entry and it's relevant fields based on whether the entry is a work order, purchase order, or general entry
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

#endpoint to modify an entry
@application.route("/entries/modify",methods=['PUT'])
def modifyEntry():
 #return an error if no user is logged in, no organization is logged in, or if the current user doesn't have permission to read these work orders
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
    #return an error if the id of the entry to modify is not given or not valid
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
    #construct and execute command to get the type of entry so that modification can be modified accordingly
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
    #If the entry is a work order, make sure it's status and completion date get updated
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
    #if the entry is a purchase order, make sure the status and purchase_ordercol get updated if necessary
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
    #Construct and execurte command to update the entry based on which fields were passed in to be updated
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

#Endpoint to remove an entry based on its ID
@application.route("/entries/remove",methods=['DELETE'])
def removeEntry():
    #return an error if no user is logged in, no organization is logged in, or if the current user doesn't have permission to read these work orders
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
    #Get the type of entry to delete, if it exists
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
    #Delete entry from list of work orders/purchase orders if it fits in either category
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
    #Delete entry from list of all entries
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

#Endpoitn to get contacts related to a given organization
@application.route("/contacts",methods=['GET'])
def getContacts():
    #Return an error if no user or org is logged in or if the user doesnt have permission
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
    #Construcr and execute query to get contacts
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT contact_id, name, company_name, d_type FROM contact ")
    command.append("WHERE organization_id=%s" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND name LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    #Return worning and empty array if no contacts exist
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


#takes a name, company_name, and a contact_type
@application.route("/contacts/new",methods=['POST'])
def addNewContact():
    #Return an error if no user, org, or if user doesn't have permission
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
    #Construct list of argumetns to be added to the new contact
    argsPresent = ['organization_id']
    valuesPresent = [str(session['org'])]
    #If a name, company_name, and contact_type are given, add them to the contact.
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
    #Construct and execute SQL command to add the contact's basic information
    cur = mysql.get_db().cursor()
    command = []
    command.append("INSERT INTO contact (%s) " % (', '.join(argsPresent),)) 
    command.append("VALUES (%s)" % (', '.join(valuesPresent),))
    cur.execute(''.join(command))
    contactID = cur.lastrowid
    #Concacts can be suppliers, contractors, or both. Insert the contact into the appropritate table in the database based on this type
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
    if(contactType == 'BTH'):
        command = []
        command.append("INSERT INTO supplier (contact_id) ")
        command.append("VALUES (%s)" % (contactID,))
        cur.execute(''.join(command))
        
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

#Get all contacts that are of type 'supplier'
@application.route("/contacts/supplier",methods=['GET'])
def getAllSupliers():
 #Return an error if no user, org, or if user doesn't have permission
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
    #Construcrt and execute SQL command to get the suppliers
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT contact_id, name, company_name FROM contact ")
    command.append("WHERE organization_id=%s AND d_type='SPP'" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND name LIKE '%%%s%%'" % (filter,))
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

#get all contacts that are of type 'contractor'
@application.route("/contacts/contractor",methods=['GET'])
def getAllContractors():
     #Return an error if no user, org, or if user doesn't have permission
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
    #Construct and execute SQL command to get contractors
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT contact_id, name, company_name FROM contact ")
    command.append("WHERE organization_id=%s AND d_type='CNT'" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND name LIKE '%%%s%%'" % (filter,))
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

#Get a single contact based on its ID
@application.route("/contacts/view",methods=['GET'])
def showOneContact():
 #Return an error if no user, org, or if user doesn't have permission
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
    #Return an error if the id for the contact doesn't exist or is invalid
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
    #Select the appropriate concact to grab info for if it exists
    cur = mysql.get_db().cursor()
    data = (session['org'], contactID)
    command = []
    command.append("SELECT contact_id, name, company_name FROM contact ")
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    result = {'info' : cur.fetchone()}
    if not result['info']:
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    data = (contactID,)
    #Get contacrt's email information and store it in result
    command = []
    command.append("SELECT email.email_id, email.email, contact_email.priority FROM email ")
    command.append("INNER JOIN contact_email ON email.email_id = contact_email.email_id ")
    command.append("WHERE contact_email.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['email'] = cur.fetchall()
    #get conrtact's phone info and store it in result
    command = []
    command.append("SELECT phone_number.phone_number_id, phone_number.phone_number, phone_number.type, contact_phone_number.priority FROM phone_number ")
    command.append("INNER JOIN contact_phone_number ON phone_number.phone_number_id = contact_phone_number.phone_number_id ")
    command.append("WHERE contact_phone_number.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['phone'] = cur.fetchall()
    #Cet contact's address info and store it in result
    command = []
    command.append("SELECT address.address_id, address.address, address.zipcode, address.city, contact_address.priority FROM address ")
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

#modifies a contact to give it access points (email, phoneNums, Addresses)
#data from js should be in the form
#emails:{emailString:"", email_priority:"Might be a num or string? Not sure how js works"}
#contactID:contact ID to have stuff added to. 
#phoneNums and addresses are similar to emails. 

#TODO - not sure this is callable from javascript. split into 3 and dont allow for multiple. 

#Post email for a contact into that contact's entry in db. See above comment for exact syntax for sending data
@application.route("/contacts/give_access_point/email",methods=['POST'])
def giveContactEmail():
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
    if not ('contact_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No contact_id given'
        )
    contactID = request.form['contact_id']
    if not contactID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given contact_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], CONTACT_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], contactID)
    command = []
    command.append("SELECT contact_id FROM contact ")
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    command.append("INSERT INTO email (email) ")
    command.append("VALUES ('%s')" % request.form.get('email'))
    cur.execute(''.join(command))
    emailID = cur.lastrowid
    command = []
    command.append("INSERT INTO contact_email (contact_id, email_id, priority) ")
    command.append("VALUES (%s, %s, %s)" % (contactID, emailID, request.form.get('priority')))
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        contact_edited=contactID
    )

#Post phone info for a contact into that contact's entry in db. See above comment for exact syntax for sending data
@application.route("/contacts/give_access_point/phone",methods=['POST'])
def giveContactPhone():
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
    if not ('contact_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No contact_id given'
        )
    contactID = request.form['contact_id']
    if not contactID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given contact_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], CONTACT_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], contactID)
    command = []
    command.append("SELECT contact_id FROM contact ")
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    command.append("INSERT INTO phone_number (phone_number, type) ")
    command.append("VALUES ('%s', '%s')" % (request.form.get('number'), request.form.get('type')))
    cur.execute(''.join(command))
    phoneNumberID = cur.lastrowid
    command = []
    command.append("INSERT INTO contact_phone_number (contact_id, phone_number_id, priority) ")
    command.append("VALUES (%s, %s, %s)" % (contactID, phoneNumberID, request.form.get('priority')))
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        contact_edited=contactID
    )

#Post address for a contact into that contact's entry in db. See above comment for exact syntax for sending data
@application.route("/contacts/give_access_point/address",methods=['POST'])
def giveContactAddress():
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
    if not ('contact_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No contact_id given'
        )
    contactID = request.form['contact_id']
    if not contactID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given contact_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], CONTACT_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    cur = mysql.get_db().cursor()
    data = (session['org'], contactID)
    command = []
    command.append("SELECT contact_id FROM contact ")
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    command.append("INSERT INTO address (address, zipcode, city) ")
    command.append("VALUES ('%s', '%s', '%s')" % (request.form.get('address'), request.form.get('zipcode'), request.form.get('city')))
    cur.execute(''.join(command))
    addressID = cur.lastrowid
    command = []
    command.append("INSERT INTO contact_address (contact_id, address_id, priority) ")
    command.append("VALUES (%s, %s, %s)" % (contactID, addressID, request.form.get('priority')))
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        contact_edited=contactID
    )
#endpoint to modify a contact
@application.route("/contacts/modify",methods=['PUT'])
def modifyContact():
    #If no user or org is logged in, throw an error. Also throw error if user doesn't haver permission to do this
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
    #Throw error if given contact id doesn't exist or is invalid
    if not ('contact_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No entry_id given'
        )
    contact_id = request.form['contact_id']
    if not contact_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message='The given contact_id was not a valid positive integer'
        )
    if not checkPermission(session['perm'], CONTACT_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #Query database for contact to modify. Throw an error if it doesn't exist
    cur = mysql.get_db().cursor()
    data = (session['org'], contact_id)
    command = []
    command.append("SELECT contact_id FROM contact ") 
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    if not cur.fetchone():
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    columns = []
    command.append("UPDATE contact SET ")
    #Update contact's respecrtive fields contact_id, name, and company_name if necessary
    if 'contact_id' in request.form:
        if request.form['contact_id'] != 'NULL':
            columns.append("contact_id = '%s'" % (request.form['contact_id'],))
        else:
            columns.append("contact_id = NULL")
    if 'name' in request.form:
        if request.form['name'] != 'NULL':
            columns.append("name = '%s'" % (request.form['name'],))
        else:
            columns.append("name = NULL")
    if 'company_name' in request.form:
        if request.form['company_name'] != 'NULL':
            columns.append("company_name = '%s'" % (request.form['company_name'],))
        else:
            columns.append("company_name = NULL")
    if columns:
        command.append(', '.join(columns))
        command.append(" WHERE contact_id=%s" % contact_id)
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        contact_edited=contact_id
    )
    
#Endpoint to remove conatac based on a given ID number
@application.route("/contacts/remove",methods=['DELETE'])
def removeContact():
    #Return an error if there's no user in session, no organizaiton, 
    #user doesn't have permission, or if the contact id either doesn't exist or is invalid
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
    if not ('contact_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No contact_id given'
        )
    contactID = request.form['contact_id']
    if not contactID.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id was not a valid positive integer"
        )
    if not checkPermission(session['perm'], CONTACT_REMOVE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #query for the user rto be removed. Return an error if it doesn't exisrt
    cur = mysql.get_db().cursor()
    data = (session['org'], contactID)
    command = []
    command.append("SELECT contact_id, d_type FROM contact ")
    command.append("WHERE organization_id=%s AND contact_id=%s" % data)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given contact_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    tag = result[1]
    data = (contactID,)
    #If the contact is a supplier, remove them from the supplier table
    if(tag == 'SPP'):
        command = []
        command.append("DELETE FROM supplier ")
        command.append("WHERE contact_id=%s" % data)
        cur.execute(''.join(command))
        
        supplierID = cur.lastrowid
        
        command = []
        command.append("DELETE FROM supplier_to_type ")
        command.append("WHERE supplier_id = %s;" % (supplierID,))
        cur.execute(''.join(command))
        
    #If the conrtact is a supplier, remove them from the supplier table
    elif(tag == 'CNT'):
        command = []
        command.append("DELETE FROM contractor ")
        command.append("WHERE contact_id=%s" % data)
        cur.execute(''.join(command))
        
        contractorID = cur.lastrowid
        
        command = []
        command.append("DELETE FROM contractor_to_type ")
        command.append("WHERE contractor_id = %s;" % (contractorID,))
        cur.execute(''.join(command))
    #If contact is a supplier and a contractor, remove them from both tables
    elif(tag == 'BTH'):
        # If they're both, they're in both tables
        command = []
        command.append("DELETE FROM supplier ")
        command.append("WHERE contact_id=%s" % data)
        cur.execute(''.join(command))
        
        supplierID = cur.lastrowid
        
        command = []
        command.append("DELETE FROM supplier_to_type ")
        command.append("WHERE supplier_id = %s;" % (supplierID,))
        cur.execute(''.join(command))
        
        command = []
        command.append("DELETE FROM contractor ")
        command.append("WHERE contact_id=%s" % data)
        cur.execute(''.join(command))
        
        contractorID = cur.lastrowid
        
        command = []
        command.append("DELETE FROM contractor_to_type ")
        command.append("WHERE contractor_id = %s;" % (contractorID,))
        cur.execute(''.join(command))
        
    #delete contact from the general contacts table
    command = []
    command.append("DELETE FROM contact ")
    command.append("WHERE contact_id=%s" % data)
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        removed_entry_id=contactID
    )

#@application.route("/about")

#@application.route("/about/axolDev")

#@application.route("/about/ezManage")

#@application.route("/help",methods=['GET'])

#@application.route("/help/search?=<filter>",methods=['GET'])

#@application.route("/help/<tutorialID>",methods=['GET'])

#Endpoint for adding a new user.
@application.route("/account/new",methods=['POST'])
def addNewUser():
    #get the email of the user to be used as their username
    email = request.form.get("userEmail")
    userExists = checkToSeeIfUserExists(email)
    #return an error if the user to be added already exists
    if(userExists):
        return jsonify(
            key=ERROR_KEY,
            message='That user already exists'
        )
    user_type = request.form.get("userType")
    #Get teh type of user. If they're an organization, give them full permissions.
    #If not, then they are an employee.
    if(user_type == "ORG"):
        access = FULL_PERMISSIONS
    else:
	#If no user is logged in/no org logged in/user doesn't have permissions, throw an error
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
	#Principle of lest privlige: Start users with no permission and add as necessary
        access = 0
    #Add user to the database with its related values
    cur = mysql.get_db().cursor()
    data = (email, request.form.get('google_client_id'), access, user_type)
    command = []
    command.append("INSERT INTO user (username, google_client_id, access, d_type) ")
    command.append("VALUES('%s', '%s', %s, '%s')" % data)
    cur.execute(''.join(command))
    userID = cur.lastrowid
    #If the user is an organization, enter them in the the organization table
    if(user_type == "ORG"):
        data = (userID, request.form['org_name'])
        command = []
        command.append("INSERT INTO organization (user_id, organization_name) ")
        command.append("VALUES (%s, '%s')" % data)
        cur.execute(''.join(command))
    #If the user is an employee, enter them into the employee table if they don't already exist. 
    elif(user_type == 'EMP'):
        employee_id = request.form.get('employee_id', None)
        if employee_id:
            data = (session['org'], employee_id)
            command = []
            command.append("SELECT employee_id FROM employee ")
            command.append("WHERE organization_id=%s AND employee_id=%s" % (data))
            cur.execute(''.join(command))
            if not cur.fetchone():
                return jsonify(
                    key=ERROR_KEY,
                    message='Employee either does not exist or does not belong to the organization'
                )
        else:
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

#Get all employees of a particular organization
@application.route("/account/personnel",methods=['GET'])
def getAllEmployees():
    #If user is not logged in/org not logged in/user no permission, throw error
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
    #Get employees based on the organization id passed in
    cur = mysql.get_db().cursor()
    data = (session['org'],)
    command = []
    command.append("SELECT employee_id, first_name, last_name, postiion FROM employee ")
    command.append("WHERE organization_id=%s" % data)
    filter = request.args.get('filter', '')
    if filter != '':
        command.append(" AND last_name LIKE '%%%s%%'" % (filter,))
    cur.execute(''.join(command))
    result = cur.fetchall()
    cur.close()
    #If organizatino has no employees, return a warning and empty array
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

#3ndpoint to add a new employee given an organization ID for the user's org, a first name, last name, and title
@application.route("/account/personnel/new",methods=['POST'])
def addEmployee():
    #throw an error if no one is logged in, no org is logged in, or user don't have permission
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
    #request data to be put into database
    data = (session['org'], request.form.get("fName"), request.form.get("lName"), request.form.get("title"))
    command = []
    #insert new employee into database
    command.append("INSERT INTO employee (organization_id, first_name, last_name, position) ")
    command.append("VALUES (%s, '%s', '%s', '%s')" % (data))
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        data=result
    )

#Get a single employee based on their ID and organization ID
@application.route("/account/personnel/view",methods=['GET'])
def showOneEmployee():
    #Throw an error if no user is logged in, if no org is logged in,
    #if the employee ID given is nonexistant or invalid,
    #or if the user doesn't have permission to perform this operation
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
    #use teh given employee ID to get the corresponding employee
    cur = mysql.get_db().cursor()
    data = (session['org'], employee_id)
    command = []
    command.append("SELECT employee_id, first_name, last_name, position FROM employee ")
    command.append("WHERE organization_id=%s AND employee_id=%s" % data)
    cur.execute(''.join(command))
    result = {info : cur.fetchone()}
    #Return an error if the employee doesn't exist
    if not result['info']:
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    data = (employee_id,)
    #Get the employee's email and store it in result
    command = []
    command.append("SELECT email.email_id, email.email, employee_email.priority FROM email ")
    command.append("INNER JOIN employee_email ON email.email_id = employee_email.email_id ")
    command.append("WHERE employee_email.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['email'] = cur.fetchall()
    #get the employees phone info and store in result
    command = []
    command.append("SELECT phone_number.phone_number_id, phone_number.phone_number, phone_number.type, employee_phone_number.priority FROM phone_number ")
    command.append("INNER JOIN employee_phone_number ON phone_number.phone_number_id = employee_phone_number.phone_number_id ")
    command.append("WHERE employee_phone_number.contact_id=%s" % data)
    cur.execute(''.join(command))
    result['phone'] = cur.fetchall()
    #get the employees address info and store it in result
    command = []
    command.append("SELECT address.address_id, address.address, address.zipcode, address.city, employee_address.priority FROM address ")
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

#Modify a user of the system given their employee id and org id
@application.route("/account/personnel/modify",methods=['PUT'])
def modifyPersonnel():
    #Throw an error if no user is logged in, if no org is logged in,
    #if the employee ID given is nonexistant or invalid,
    #or if the user doesn't have permission to perform this operation
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
    if not ('employee_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No employee_id given'
        )
    employee_id = request.form['employee_id']
    if not employee_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id was not a valid positive integer"
        )
    if not checkPermission(session['perm'], PERSONNEL_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #get the employee to be updated based on their id and org id
    cur = mysql.get_db().cursor()
    data = (session['org'], employee_id)
    command = []
    command.append("SELECT employee_id FROM employee ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE organization_id=%s AND employee_id=%s" % data)
    cur.execute(''.join(command))
    #return an error if the user doesnt exist or isnt in this organization
    if not cur.fetchone():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    columns = []
    #update employee first name if necessary
    command.append("UPDATE employee SET ")
    if 'first_name' in request.form:
        if request.form['first_name'] != 'NULL':
            columns.append("first_name = '%s'" % (request.form['first_name'],))
        else:
            columns.append("first_name = NULL")
    #update last name if necessary
    if 'last_name' in request.form:
        if request.form['last_name'] != 'NULL':
            columns.append("last_name = '%s'" % (request.form['last_name'],))
        else:
            columns.append("last_name = NULL")
    #update title if necessary
    if 'position' in request.form:
        if request.form['position'] != 'NULL':
            columns.append("position = '%s'" % (request.form['position'],))
        else:
            columns.append("position = NULL")
    if columns:
        command.append(', '.join(columns))
        command.append(" WHERE employee_id=%s" % employee_id)
        cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        employee_edited=employee_id
    )

#remove an employee based on their id and org id
@application.route("/account/personnel/remove",methods=['DELETE'])
def removeEmployee():
    #Throw an error if no user is logged in, if no org is logged in,
    #if the employee ID given is nonexistant or invalid,
    #or if the user doesn't have permission to perform this operation
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
    if not ('employee_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No employee_id given'
        )
    employee_id = request.form['employee_id']
    if not employee_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id was not a valid positive integer"
        )
    if not checkPermission(session['perm'], PERSONNEL_REMOVE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #get the user to delete based on their ID and org id
    cur = mysql.get_db().cursor()
    data = (session['org'], employee_id)
    command = []
    command.append("SELECT employee_id FROM employee ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE organization_id=%s AND employee_id=%s" % data)
    cur.execute(''.join(command))
    #return an error if the user doeasn't exist or isnt in this org
    if not cur.fetchone():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    command.append("SELECT user_id FROM employee_user ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE employee_id=%s" % employee_id)
    cur.execute(''.join(command))
    if not cur.fetchone():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id is a user and cannot be properly removed"
        )
    command = []
    command.append("DELETE FROM employee ")
    command.append("WHERE employee_id=%s" % data)
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        removed_employee_id=employee_id
    )

#edpoint to get the username of the user currently logged in using 'session'
@application.route("/account/username",methods=['GET'])
def getUserName():
    #If no user is logged in, return an error
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    #get the current user's username and return it
    cur = mysql.get_db().cursor()
    command = []
    command.append("SELECT username FROM user ")
    command.append("WHERE user_id = %s"% session['user'])
    cur.execute(''.join(command))
    result = cur.fetchone()
    return jsonify(
	key=SUCCESS_KEY,
	data=result
    )

#endpoint to be used by organization/managers for getting all personnel info and their respective permission levels
@application.route("/account/personnel/permissions",methods=['GET'])
def getAllUserEmployees():
    #Throw an error if no user is logged in, if no org is logged in,
    #or if the user doesn't have permission to perform this operation
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
    #get and return relevant employee information from the database
    cur = mysql.get_db().cursor()
    command = []
    command.append("SELECT e.employee_id, u. user_id, e.first_name, e.last_name, e.position, u.username, u.access  ")
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

#Endpoint to modify a user's permissions
@application.route("/account/personnel/permissions/modify",methods=['PUT'])
def updatePermission():
    #If no user is logged in, return an error
    if not ('user' in session):
        return jsonify(
            key=ERROR_KEY,
            message='No user is logged in'
        )
    #if no org is logged in, return an error
    if not ('org' in session):
       return jsonify(
            key=ERROR_KEY,
            message='User logged in is not an employee or organization'
        )
    #if the employee id is not given ,return an error
    if not ('employee_id' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No employee_id given'
        )
    #If the user id is not valid, return an error
    employee_id = request.form['employee_id']
    if not employee_id.isdigit():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id was not a valid positive integer"
        )
    #if no permission levels are given, throw an error
    if not ('access' in request.form):
        return jsonify(
            key=ERROR_KEY,
            message='No access given'
        )
    #If permission levels given are invalid (more than full permissions, negative permissions, etc), throw an error
    access = request.form['access']
    if not (access.isdigit() and int(access) >= 0 and int(access) <= FULL_PERMISSIONS):
        return jsonify(
            key=ERROR_KEY,
            message="The given access was not a valid positive integer"
        )
    #If trhe current user does not have permission to change permissions, throw an error
    if not checkPermission(session['perm'], PERMISSION_WRITE):
        return jsonify(
            key=ERROR_KEY,
            message='User does not have the permission'
        )
    #get the user whose permissions will be changed based on their employye id and org id
    cur = mysql.get_db().cursor()
    data = (session['org'], employee_id)
    command = []
    command.append("SELECT employee_id FROM employee ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE organization_id=%s AND employee_id=%s" % data)
    cur.execute(''.join(command))
    #if the user doesnt exist or is not in this org, throw an error
    if not cur.fetchone():
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id either does not belong to the logged in user's organization, or does not exist at all"
        )
    command = []
    command.append("SELECT user_id FROM employee_user ") #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE employee_id=%s" % employee_id)
    cur.execute(''.join(command))
    result = cur.fetchone()
    if not result:
        return jsonify(
            key=ERROR_KEY,
            message="The given employee_id is not a user"
        )
    user_id = result[0]
    #update the user's permission levels
    command = []
    command.append("UPDATE user SET access=%s " % access) #command.append("SELECT entry_id, d_type FROM entry ")
    command.append("WHERE user_id=%s" % user_id)
    cur.execute(''.join(command))
    mysql.get_db().commit()
    cur.close()
    return jsonify(
        key=SUCCESS_KEY,
        user_edited=user_id
    )

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=80)

