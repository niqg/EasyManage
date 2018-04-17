function getFilteredWorkOrders(input) {
    $.ajax({
        url: '/entries/work',
        type: 'GET',
        data: {
        filter: input,
        },
success: function(data) {
        console.log("The Search Work Entry Script has finished");

        //panel where the table is inserted
            var panel = document.getElementById("panelBody");

            // Find a <table> element with id="myTable":
            var table = document.getElementById("tableid");
            table.innerHTML = "";
            // Create an empty <thead> element and add it to the table:
            var header = table.createTHead();

            // Create an empty <tr> element and add it to the first position of <thead>:
            var row = header.insertRow(0);

            // Insert a new cell (<td>) at the first position of the "new" <tr> element:
            var cell = row.insertCell(0);
            var cell1 = row.insertCell(1);
            var cell2 = row.insertCell(2);
            var cell3 = row.insertCell(3);
            var cell4 = row.insertCell(4);
            var cell5 = row.insertCell(5);

            // Add some bold text in the new cell:
            cell.innerHTML = "<b>Entry ID</b>";
            cell1.innerHTML = "<b>Title</b>";
            cell2.innerHTML = "<b>Date Created</b>";
            cell3.innerHTML = "<b>Status</b>";
            cell4.innerHTML = "<b>Date Completed</b>";
            cell5.innerHTML = "<b>Description</b>";
            cell5.width = "40%"
	    var contentHeader = document.getElementById("entryHeader");
    		contentHeader.innerHTML = "Work Orders";
                          var json = data.data
	tblbody = document.createElement("tbody");
            for(var i = 0; i < json.length; i++) {
                var obj = json[i];

                var row = tblbody.insertRow();
                var cell0 = row.insertCell(0);
                var cell1 = row.insertCell(1);
                var cell2 = row.insertCell(2);
                var cell3 = row.insertCell(3);
                var cell4 = row.insertCell(4);
                var cell5 = row.insertCell(5);

                cell0.innerHTML = obj[0];	//entry ID
                cell1.innerHTML = obj[1];	//Title
                cell2.innerHTML =  obj[2];	//date created
                cell3.innerHTML =  obj[4]; //status (completed or not)
                cell4.innerHTML =  obj[5]; //Type
                cell5.innerHTML =  obj[3];	//description
	
	    table.appendChild(tblbody);
        }

        //panel.appendChild(table); //adds the final table to the panel body
        //document.getElementById('result').value = "test";
    }
    
    });
}
