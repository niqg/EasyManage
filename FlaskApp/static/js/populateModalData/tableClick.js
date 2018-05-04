function tableClick(){
	console.log("table click script has fired");
	 var table = document.getElementById("tbody");
         var state = getState();
        console.log("TEST: I clicked the table and the state is " +state);
	if(state === "Settings"){
		return;
		}
	if(state === "Contacts"){
		console.log("WE ARE ON THE CONTACTS PAGE RIGHT NOW");
		for (var i = 0; i < table.rows.length; i++) {
            for (var j = 0; j < table.rows[i].cells.length; j++) 
				table.rows[i].onclick = function () {
				//this gets each data element from table
				var $tds = $(this).find('td'),
				contactID = $tds.eq(0).text(),
				company = $tds.eq(1).text(),
				type = $tds.eq(3).text();
				console.log("THE TYPE IS : " + type);
				//number = $tds.eq(3).text();
				//email = $tds.eq(4).text();
				//console.log(name);
				//console.log(company);
				//console.log(type);
				//console.log(number);
				//console.log(email);
				//var contactInfo = getContact(58);
				//console.log(contactInfo);
				populateModifyContactModal(contactID, type);
				//} 
				var mymodal = $('#modifyContactModal');
				//populateModalData(entryID, title, description);
				mymodal.show();
            };
        }
			
		}
	else{
    if (table != null) {
        for (var i = 0; i < table.rows.length; i++) {
            for (var j = 0; j < table.rows[i].cells.length; j++)
				table.rows[i].onclick = function () {
				//this gets each data element from table
				var $tds = $(this).find('td'),
				entryID = $tds.eq(0).text(),
				//fake = $tds.eq(1).text(),
				title = $tds.eq(1).text(),
				date = $tds.eq(2).text();
				if(state === "Entries"){
					type = $tds.eq(3).text();
					description = $tds.eq(4).text();
				console.log("entry type = entries fired");
					//populateEntriesModalData(entryID, title, date, type, description);
					populateModifyEntryModal(entryID, title, type, date, "N/A", "N/A",
								"N/A", description);
				} else if(state === "Work Orders"){
					statusOf  = $tds.eq(3).text();
					//console.log("status is " + statusOf);
					//console.log("entry type = wrk order fired");
					dateCompleted = $tds.eq(4).text();
					description  = $tds.eq(4).text();
					//populateWorkOrdersModalData(entryID, title, date, statusOf, dateCompleted, description);
					populateModifyEntryModal(entryID, title, "N/A", date, statusOf, dateCompleted,
                                                                "N/A", description);
				} else if(state === "Purchase Orders"){
					//console.log("entry type = prc order fired");
                                        statusOf = type = $tds.eq(3).text();
                                        purchaseCost = $tds.eq(4).text();
                                        description  = $tds.eq(4).text();
                                        populateModifyEntryModal(entryID, title, "N/A", date, statusOf, "N/A",
                                                                purchaseCost, description);
					//populatePurchaseOrdersModalData(entryID, title, date, status, purchaseCost, description);
				} else if(state === "General Orders"){
					console.log("entry type = general");
                                        description  = $tds.eq(3).text();
                                        console.log("this shouldt fire");
					// populateGeneralOrdersModalData(entryID, title, date, description);
					populateModifyEntryModal(entryID, title, "N/A", date, "N/A", "N/A",
                                                                "N/A", description);
				}
				var mymodal = $('#modifyEntryModal');
				//populateModalData(entryID, title, description);
				mymodal.show();
            };
        }
    }
    }

    

}
