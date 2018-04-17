var firstNameTextArea = document.createElement('input');
firstNameTextArea.type = "text";

var lastNameTextArea = document.createElement('input');
lastNameTextArea.type = "text";

var jobTitleTextArea = document.createElement('input');
jobTitleTextArea.type = "text";

var emailTextArea = document.createElement('input');
emailTextArea.type = "text";

var submitNewUserButton = document.createElement('input');
submitNewUserButton.type = "button";
submitNewUserButton.className = "btn";
submitNewUserButton.value = "Add User";

submitNewUserButton.onclick = submitUser;

var emailToAccess = {};
var emailToId = {};

var settingsButton = document.getElementById("settingButton");
settingsButton.onclick = getSettings;


function getSettings() {
    setState("Settings");
    toggleCalendar(); 
    //toggleCalendar();
    var table = document.getElementById("tableid");
    table.innerHTML = "";
    var contentHeader = document.getElementById("entryHeader");
    contentHeader.innerHTML = "Settings";
    console.log("Settings Script has been fired");
    
    var input = document.createElement('input');
    /*
    var header = table.createTHead();
    
    //headers
    var row1 = header.insertRow();

    var title1 = row1.insertCell(0);
    var title2 = row1.insertCell(1);
    var title3 = row1.insertCell(2);
    var title4 = row1.insertCell(3);
    var title5 = row1.insertCell(4);
    
    title1.value = '<b>First Name</b>';
    title2.value = '<b>Last Name</b>';
    title3.value = '<b>Title</b>';
    title4.value = '<b>Email</b>';
    title5.value = '';*/
    
    
    var firstName = document.createElement('input');
    firstName.type = "text";
    var middleInitial = document.createElement('input');
    middleInitial.type = "text";
    var lastName = document.createElement('input');
    lastName.type = "text";
    var email = document.createElement('input');
    email.type = "text";
    
    var submitButton = document.createElement('input');
    submitButton.type = "button";
    submitButton.className = "btn";
    submitButton.value = "Add user";
    
    
    //add Header
    appendToTable('<b>First Name</b>', '<b>Last Name</b>','<b>Title</b>', '<b>Email</b>', '');
    
    
    
    //appendToTable(table, '<input type="text" id="FirstName"> </input>', lastName, '', '', '');
    var header = table.createTHead();
    var row2 = header.insertRow(1);
    
    var fNameArea = row2.insertCell(0);
    var lNameArea = row2.insertCell(1);
    var titleArea = row2.insertCell(2);
    var emailArea = row2.insertCell(3);
    var buttonArea = row2.insertCell(4);
    
    fNameArea.appendChild(firstNameTextArea);
    lNameArea.appendChild(lastNameTextArea);
    titleArea.appendChild(jobTitleTextArea);
    emailArea.appendChild(emailTextArea);
    buttonArea.appendChild(submitNewUserButton);
    	$.ajax({
	      url: '/account/personnel/permissions',
        type: 'GET',
	      data: {},
        success: function(data) {
        console.log("The Get user settings Script has finished");
        
        
        	if(data.key === 1){
                console.log("the Data key was " + data.key + "...aborting");
                var table = document.getElementById("tableid");
		            table.innerHTML = data.message;
                return;
            }	
         var json = data.data;
         
         emailToAccess = {};
         emailToId = {};
         
         for(var i = 0; i < json.length; i++) {
            var obj = json[i];
            //objects 0-4 are fname, lname, title, email, and access/permissions (in that order)
            var row = appendToTable(obj[2], obj[3], obj[4], obj[5]);
            
            emailToAccess[obj[5]] = obj[6];  //create a map/dictionary from email to access ability. 
            
            emailToId[obj[5]] = obj[0];
            
            row.addEventListener("click", displayAccessOptions);
            
         }
      }});
      
     firstNameTextArea.value = "";
     lastNameTextArea.value = "";
     jobTitleTextArea.value = "";
     emailTextArea.value = ""; 
}


//TODO one two three and four are terrible names. refactor them. 
function appendToTable(one, two, three, four)
{
    var table = document.getElementById("tableid");
    var header = table.createTHead();
    var row = header.insertRow();
    
    var oneText = row.insertCell(0);
    var twoText = row.insertCell(1);
    var threeText = row.insertCell(2);
    var fourText = row.insertCell(3);    
    
    oneText.innerHTML = one;
    twoText.innerHTML = two;
    threeText.innerHTML = three;
    fourText.innerHTML = four;
    
    return row;   

}


function submitUser(event)
{
    var firstName = firstNameTextArea.value;
    var lastName = lastNameTextArea.value;
    var jobTitle = jobTitleTextArea.value;
    var email = emailTextArea.value;
    
    if(!validateEmail(email) || firstName === "" || lastName === "" || jobTitle === "") {
        // TODO MAKE THAT POPUP SAYING YO THIS EMAIL SUCKS FIX YO STUFF
        window.alert("You messed up");
        return ;
    }
    
    //appendToTable(firstNameTextArea.value, lastNameTextArea.value,jobTitleTextArea.value, emailTextArea.value);
    $.ajax({url:"/account/new", type: "POST", data: {google_client_id:email, userEmail:email, userType:"EMP", fName:firstName, lName:lastName, title:jobTitle}, success: function(data) {}});    
    
    getSettings();
    
}

//sourced from https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}


function onSignIn(googleUser)
{
    console.log("Getting email works!")
}

var currentEmail;

function displayAccessOptions(event)
{
    var row = event.currentTarget;
    var rowArray = row.getElementsByTagName("td");
    
    var email = rowArray[3].innerText;
    currentEmail = email;
    var access = emailToAccess[email];

    console.log(access);
  
    var settingsModal = document.getElementById('settingsModal');
    var closeModal = document.getElementById('closeSettingsModal');

    settingsModal.style.display = "block";
    
    closeModal.onclick = function(){
        settingsModal.setAttribute("style.display","none");
    }
    window.onclick = function(event) {
        if (event.target == settingsModal) {
            settingsModal.style.display = "none";
        }
    }
    
    populateCheckboxes(access);
    
}

function getPermissionCheckboxes(){
     var permCheckboxes = [];

    for(var i = 1; i<=11; i++){
        permCheckboxes.push(document.getElementById('permission' + i));
    }

    return permCheckboxes;
}

function populateCheckboxes( access){
  
  var permissionCheckboxes = getPermissionCheckboxes();
    for(var i = 0; i<=10; i++){
        if((access % 2) == 0)
        {
              permissionCheckboxes[i].checked = false;
              //permissionCheckboxes[i].setAttribute("checked","false");
        }
        else{
            //permissionCheckboxes[i].setAttribute("checked","true");
                    permissionCheckboxes[i].checked = true;
        }
	      access = access >> 1;
    }
}

function applyPermissions()
{
    var access = 0;
    var currentPermission = 1024;
    var permissionCheckboxes = getPermissionCheckboxes();
    for(var i = 0; i<=10; i++)
    {
        if(permissionCheckboxes[i].checked)//permission box is checked. 
        {
            access = access | currentPermission;
        }
        if(i != 10)
        {
            access = access >> 1;
        }
    }
    console.log(access);
    
    var empId = emailToId[currentEmail];
    console.log(empId);
    
    $.ajax({url:"/account/personnel/permissions/modify", type: "PUT", data: {employee_id:empId, access:access}, success: function(data) {
    console.log(data.message);
    console.log(data.user_edited);
    }});
    
    var settingsModal = document.getElementById('settingsModal');
    settingsModal.style.display = "none";
    
    emailToAccess[currentEmail] = access;

}

