function tableClick(){
	console.log("table click script has fired");
	 var table = document.getElementById("tableid");
    if (table != null) {
        for (var i = 0; i < table.rows.length; i++) {
            for (var j = 0; j < table.rows[i].cells.length; j++)
				table.rows[i].onclick = function () {
				//this gets each data element from table
				var entryType = document.getElementById("entryHeader").innerHTML;
				console.log("THE HEADER IS " + entryType);
				var $tds = $(this).find('td'),
				entryID = $tds.eq(0).text(),
				title = $tds.eq(1).text(),
				date = $tds.eq(2).text();
				if(entryType === "Entries"){
					type = $tds.eq(3).text();
					description = $tds.eq(4).text();
					console.log("entry type = entries fired");
					populateEntriesModalData(entryID, title, date, type, description);
				} else if(entryType === "Work Orders"){
					statusOf  = $tds.eq(3).text();
					console.log("status is " + statusOf);
					console.log("entry type = wrk order fired");
					dateCompleted = $tds.eq(4).text();
					description  = $tds.eq(5).text();
					populateWorkOrdersModalData(entryID, title, date, statusOf, dateCompleted, description);
				} else if(entryType === "Purchase Orders"){
					console.log("entry type = prc order fired");
                                        status = type = $tds.eq(3).text();
                                        purchaseCost = $tds.eq(4).text();
                                        description  = $tds.eq(5).text();
                                        populatePurchaseOrdersModalData(entryID, title, date, status, purchaseCost, description);
				} else if(entryType === "General Entries"){
					console.log("entry type = general");
                                        description  = $tds.eq(3).text();
                                       console.log("this shouldt fire");
					 populateGeneralOrdersModalData(entryID, title, date, description);	
				}
				var mymodal = $('#modifyEntryModal');
				//populateModalData(entryID, title, description);
				mymodal.show();
            };
        }
    }

    

}
