
function generate_table() {
    var title = document.getElementById('title').value;
    var date = document.getElementById('date').value;
    var description = document.getElementById('description').value;
    var entryType = document.getElementById('entryType').value;
    // get the reference for the body
    var body = document.getElementsByTagName("body")[0];

    var table = document.getElementById('example') //table in userScreen


                // Create an empty <tr> element and add it to the 1st position of the table:
                var row = table.insertRow();


    var row = document.createElement("tr");



    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);

    // Add some text to the new cells:
    cell1.innerHTML = "N/A";
    cell2.innerHTML = entryType;
    cell3.innerHTML = title;
    cell4.innerHTML = "N/A";
    cell5.innerHTML = date;
    cell6.innerHTML = description;


    table.appendChild(row);
    /* creating all cells
    for (var i = 0; i < 2; i++) {
        // creates a table row
        var row = document.createElement("tr");

        for (var j = 0; j < 2; j++) {
            // Create a <td> element and a text node, make the text
            // node the contents of the <td>, and put the <td> at
            // the end of the table row
            var cell = document.createElement("td");
            var cellText = document.createTextNode(title + date + description + entryType);
            cell.appendChild(cellText);
            row.appendChild(cell);
        }

        // add the row to the end of the table body
        tblBody.appendChild(row);
    }*/

    // put the <tbody> in the <table>

}
