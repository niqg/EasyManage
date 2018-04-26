function getEntries() { 
    setState("Entries");
    toggleCalendar(); 
   $.getJSON("/entries", {},
    function(data) {
        //var obj = JSON.parse(data.result)
        //obj.data
        console.log("The Get Entries script has been fired");

	if(data.key === 1){
                console.log("the Data key was " + data.key + "...aborting");
                var table = document.getElementById("tableid");
                 table.innerHTML = data.message;
                return;
            }
        //panel where the table is inserted
        var panel = document.getElementById("panelBody");

        // Find a <table> element with id="myTable":
        var table = document.getElementById("tableid");
        table.innerHTML = "";
        // Create an empty <thead> element and add it to the table:
        var header = table.createTHead();
	header.id = "thead";

        // Create an empty <tr> element and add it to the first position of <thead>:
        var row = header.insertRow(0);

        // Insert a new cell (<td>) at the first position of the "new" <tr> element:
     
	var cell = row.insertCell(0);
	cell.className = "col1";
	cell.innerHTML = "Entry ID";
//	var cell0 = row.insertCell(1); // fake entry ID
        var cell1 = row.insertCell(1); //Title
        var cell2 = row.insertCell(2); //date created
        var cell3 = row.insertCell(3); //type
        var cell4 = row.insertCell(4); // description

        // Add some bold text in the new cell:
	cell.setAttribute("style", "visibility: hidden");
	cell.width = "1%";
	//cell0.innerHTML = "<b>Fake Entry ID<b>";
        cell1.innerHTML = "<b>Title</b>";
        cell2.innerHTML = "<b>Date Created</b>";
        cell3.innerHTML = "<b>Type</b>";
        cell4.innerHTML = "<b>Description</b>";
        cell4.width = "40%";
	var contentHeader = document.getElementById("entryHeader");
   	 contentHeader.innerHTML = "Entries"; 
         var json = data.data;
	tblbody = document.createElement("tbody");
	tblbody.id = "tbody";
	    for(var i = 0; i < json.length; i++) {
            var obj = json[i];

            var row = tblbody.insertRow();
            var cell0 = row.insertCell(0);
	   // var cell00 = row.insertCell(1);
	    cell0.className = "col1";
	    cell0.setAttribute("style", "visibility: hidden");
	    cell0.width = "1%";
            var cell1 = row.insertCell(1);
            var cell2 = row.insertCell(2);
            var cell3 = row.insertCell(3);
            var cell4 = row.insertCell(4);
	   // cell00.innerHTML = "E" + (0000+i);
            cell0.innerHTML = obj[0];	//entry ID
            cell1.innerHTML = obj[1];	//Title
            cell2.innerHTML =  obj[2];	//date created
	   // console.log("TYPE   : " + obj[4]);
            if(obj[4] === null){
		cell3.innerHTML = "GNR";
		} else{
	    cell3.innerHTML =  obj[4]; //Type
	    }
            cell4.innerHTML =  obj[3];	//description
	
	    table.appendChild(tblbody);
	    var col1 = document.getElementsByClassName("col1");
	    
        }
	//col1
	//var att = document.createAttribute("visiblity");
	//col1.setAttribute("visibility", "hidden");
        //panel.appendChild(table); //adds the final table to the panel body
        //document.getElementById('result').value = "test";
    }
    ).fail(function() {
        console.log("Fail");
	//window.location = "http://axolotldevelopment.com/index";
    });
}
