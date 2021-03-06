
    var authorizeButton = document.createElement('input');
    authorizeButton.type = "button";
    authorizeButton.className = "btn";
    authorizeButton.value = "Access Calendar";

    var signoutButton = document.createElement('input');
    signoutButton.type = "button";
    signoutButton.className = "btn";
    signoutButton.value = "Calendar LogOut";
    
    var createEventButton = document.createElement('input');
    createEventButton.type = "button";
    createEventButton.className = "btn";
    createEventButton.value = "Add Event";
    createEventButton.onclick =  "postEvent()";
    
    var startDate = document.createElement('input');
    startDate.type = "text";
    var endDate = document.createElement('input');
    endDate.type = "text";
    var summary = document.createElement('input');
    summary.type = "text";
    var timeZone = document.createElement('input');
    timeZone.type = "text";
    var description = document.createElement('input');
    description.type = "text";
    
      //var CLIENT_ID = '69496104427-vd134aptc08qphb7gmpqd7j55mdcmjij.apps.googleusercontent.com'; //OLD
      //var CLIENT_ID = '430084226490-l250drphth8ar7922g60ner0d4mujg5o.apps.googleusercontent.com'; //our
      var CLIENT_ID = '1073267817738-e82qtpk9i1li4dd2gap3ntdd5dmq4kvn.apps.googleusercontent.com'; //mine
      //var API_KEY = 'AIzaSyB57A4LqZGLiSsYRfYLZIyBuMfY-Hbp7EA'; //OLD
      //var API_KEY = 'AIzaSyDcnW6WejpTOCffshGDDb4neIrXVUA1EAE'; //ours apperenty
      var API_KEY = 'AIzaSyBm5rtXYqmGOWklf6dBRvYhW4kI2N1n5SQ'; //mine

      // Array of API discovery doc URLs for APIs used by the quickstart
      var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"];

      // Authorization scopes required by the API; multiple scopes can be
      // included, separated by spaces.
      var SCOPES = "https://www.googleapis.com/auth/calendar";//.readonly";
      //var authorizeButton = document.getElementById('authorize-button');
      //var signoutButton = document.getElementById('signout-button');
	 //var createEventButton = document.getElementById('create-event-button');
	  //var deleteEventButton = document.getElementById('delete-event-button');

initClient(); 

      /**
       *  On load, called to load the auth2 library and API client library.
       */
      function handleClientLoad() {
        gapi.load('client:auth2', initClient);
      }

      /**
       *  Initializes the API client library and sets up sign-in state
       *  listeners.
       */
      function initClient() {
        gapi.client.init({
          apiKey: API_KEY,
          clientId: CLIENT_ID,
          discoveryDocs: DISCOVERY_DOCS,
          scope: SCOPES
        }).then(function () {
          // Listen for sign-in state changes.
          gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

          // Handle the initial sign-in state.
          updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
          authorizeButton.onclick = handleAuthClick;
          signoutButton.onclick = handleSignoutClick;
		  createEventButton.onclick = postEvent();
        });
      }

      /**
       *  Called when the signed in status changes, to update the UI
       *  appropriately. After a sign-in, the API is called.
       */
      function updateSigninStatus(isSignedIn) {
        if (isSignedIn) {
          authorizeButton.style.display = 'none';
          signoutButton.style.display = 'block';
          //listUpcomingEvents();
        } else {
          authorizeButton.style.display = 'block';
          signoutButton.style.display = 'none';
        }
      }

      /**
       *  Sign in the user upon button click.
       */
      function handleAuthClick(event) {
        gapi.auth2.getAuthInstance().signIn();
        if(gapi.auth2.getAuthInstance().isSignedIn.get()){
            listUpcomingEvents();
            }
      }

      /**
       *  Sign out the user upon button click.
       */
      function handleSignoutClick(event) {
        gapi.auth2.getAuthInstance().signOut();
      }

      /**
       * Append a pre element to the body containing the given message
       * as its text node. Used to display the results of the API call.
       *
       * @param {string} message Text to be placed in pre element.
       */
      function appendPre(summary, startDate, endDate, timeZone, description) {
          var table = document.getElementById("tableid");
          var header = table.createTHead();
          
          var row = header.insertRow();
          
              var startText = row.insertCell(0);
              var endText = row.insertCell(1);
              var summaryText = row.insertCell(2);
              var timeZoneText = row.insertCell(3);
              var descriptionText = row.insertCell(4);
              
              
          startText.innerHTML = startDate;
          endText.innerHTML = endDate;
          summaryText.innerHTML = summary;
          timeZoneText.innerHTML = timeZone;
          descriptionText.innerHTML = description;
      
        //var pre = document.getElementById('content');
        //var textContent = document.createTextNode(message + '\n');
        //pre.appendChild(textContent);
      }

      /**
       * Print the summary and start datetime/date of the next ten events in
       * the authorized user's calendar. If no events are found an
       * appropriate message is printed.
       */
      function listUpcomingEvents() {
        gapi.client.calendar.events.list({
          'calendarId': 'primary',
          'timeMin': (new Date()).toISOString(),
          'showDeleted': false,
          'singleEvents': true,
          //'maxResults': 10,
          'orderBy': 'startTime'
        }).then(function(response) {
          var events = response.result.items;
          //appendPre('Upcoming events:');

          if (events.length > 0) {
            for (i = 0; i < events.length; i++) {
              var event = events[i];
              var when = event.start.dateTime;
              if (!when) {
                when = event.start.date;
              }
              appendPre(event.summary, event.start.dateTime, event.end.dateTime, event.start.timeZone, event.description);
            }
          } else {
            //appendPre('No upcoming events found.');
          }
        });
      }

	  
	  
function postEvent() {
	console.log("Post Event script has fired");
 
	var event = {
	  'summary': 'Google I/O 2017', //summary.value,
	  'location': '800 Howard St., San Francisco, CA 94103',
	  'description':  'A chance to hear more about Google\'s developer products.', //description.value,
	  'start': {
		'dateTime': '2018-05-29T09:00:00-07:00', //(startDate.value.concat('T09:00:00-07:00')), //'2018-05-30T09:00:00-07:00',
		'timeZone': 'America/Los_Angeles' //timeZone.value 
	  },
	  'end': {
		'dateTime': '2018-06-29T17:00:00-08:00', //(endDate.value.concat('T09:00:00-07:00'))
		'timeZone': 'America/Los_Angeles' //timeZone.value
	  },
	  'recurrence': [
		'RRULE:FREQ=DAILY;COUNT=2'
	  ],
	  'attendees': [
		{'email': 'abc@gmail.com'},
		{'email': 'def@gmail.com'}
	  ],
	  'reminders': {
		'useDefault': false,
		'overrides': [
		  {'method': 'email', 'minutes': 24 * 60},
		  {'method': 'popup', 'minutes': 10}
		]
	  }
	};

	var request = gapi.client.calendar.events.insert({
	  'calendarId': 'primary',
	  'resource': event
	});

	request.execute(function(event) {
	  //appendPre('Event created: ' + event.htmlLink);
	});

	summary.value = "";
description.value = "";
startDate.value = "";
timeZone.value = "";
endDate.value = "";
	
}
function getCalendar() {
	var modal = document.getElementById("createEntryModalBody");
    ///var table = document.getElementById("tableid");
    ///table.innerHTML = "";
    ///var contentHeader = document.getElementById("entryHeader");
    //var date = document.getElementById("calendarDate");
    //date.style.display = 'none';
    ///contentHeader.innerHTML = "Calendar";
    console.log("Calendar On Modal Script has been fired");
    
    //var header = table.createTHead();
    var startDiv = document.createElement("div");
    var startInput = document.createElement('input');
    var startLabel = document.createElement('label');
    startLabel.innerHTML = "Start Date";
    startDiv.appendChild(startLabel);
    startDiv.appendChild(startInput);
    
    var endDiv = document.createElement("div");
    var endInput = document.createElement('input');
    var endLabel = document.createElement('label');
    endLabel.innerHTML = "End Date";
    endDiv.appendChild(endLabel);
    endDiv.appendChild(endInput);
    
    var summaryDiv = document.createElement("div");
    var summaryInput = document.createElement('input');
    var summaryLabel = document.createElement('label');
    summaryLabel.innerHTML = "Summary";
    summaryDiv.appendChild(summaryLabel);
    summaryDiv.appendChild(summaryInput);
    
    var tzDiv = document.createElement("div");
    var tzInput = document.createElement('input');
    var tzLabel = document.createElement('label');
    tzLabel.innerHTML = "Time Zone";
    tzDiv.appendChild(tzLabel);
    tzDiv.appendChild(tzInput);
    
    var descDiv = document.createElement("div");
    var descInput = document.createElement('input');
    var descLabel = document.createElement('label');
    descLabel.innerHTML = "Description";
    descDiv.appendChild(descLabel);
    descDiv.appendChild(descInput);
    
    modal.appendChild(startDiv);
    modal.appendChild(endDiv);
    modal.appendChild(summaryDiv);
    modal.appendChild(tzDiv);
    modal.appendChild(descDiv);
    modal.appendChild(createEventButton);
    modal.appendChild(authorizeButton);
    
    
    //headers
    ///var row1 = header.insertRow(0);

   
    ///var title1 = row1.insertCell(0);
    ///var title2 = row1.insertCell(1);
    ///var title3 = row1.insertCell(2);
    ///var title4 = row1.insertCell(3);
    ///var title5 = row1.insertCell(4);
    
    ///title1.innerHTML = '<b>Start Date (YYYY-MM-DD)</b>';
    ///title2.innerHTML = '<b>End Date(YYYY-MM-DD)</b>';
    ///title3.innerHTML = '<b>Summary</b>';
    ///title4.innerHTML = '<b>TimeZone(America/Los_Angeles)</b>';
    ///title5.innerHTML = '<b>Description</b>';

    //text boxes    
    //var row2 = header.insertRow(1);
    
    ///var startDateArea = row2.insertCell(0);
    ///var endDateArea = row2.insertCell(1);
    ///var summaryArea = row2.insertCell(2);
    ///var timeZoneArea = row2.insertCell(3);
    ///var descriptionArea = row2.insertCell(4);
    
    
    //startDateArea.appendChild(startDate);
    //endDateArea.appendChild(endDate);
    //summaryArea.appendChild(summary);
    //timeZoneArea.appendChild(timeZone);
    //descriptionArea.appendChild(description);
    
    //buttons
    //var row3 = header.insertRow(2);
    
    //var authorizeButtonArea = row3.insertCell(0);
    //var signoutButtonArea = row3.insertCell(1);
    //var createEventButtonArea = row3.insertCell(2);
    
    //authorizeButtonArea.appendChild(authorizeButton);
    //signoutButtonArea.appendChild(signoutButton);
    //createEventButtonArea.appendChild(createEventButton);   
    
    //if(gapi.auth2.getAuthInstance().isSignedIn.get()){
    //listUpcomingEvents();
    //}
    

    
    //cell2.innerHTML = '<b>Last Name:</b>';
    //cell3.innerHTML = '<input id = "lastName">';
    //cell4.innerHTML = '<button >Add Event</button>';   
}

