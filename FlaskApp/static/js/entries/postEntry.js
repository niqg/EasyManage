function postEntry() {

    console.log("Post Entry Script has been fired");

//our modal that contains the form we fill out
    var modal = document.getElementById("createEntryModal").value;
    var modalBody = document.getElementById("createEntryModalBody");   

    var titleValue = document.getElementById("createEntryTitle").value;
    var descriptionValue = document.getElementById("createEntryDescription").value;
    var dateValue = formatDate(new Date());
    var typeValue = document.getElementById("createEntryType").value;

    //console.log(titleValue);
    //console.log(dateValue);
    //console.log(descriptionValue);
    //console.log(typeValue);

    if(titleValue === ""){
	console.log("Opps, no entry inputted");
	var str = "*TITLE CAN NOT BE BLANK";
	var errorLabel = document.createElement("label");
	errorLabel.innerHTML = str;
	errorLabel.setAttribute("style", "color: red");
	modalBody.appendChild(errorLabel);
        return
	}

//Different post
    $.ajax({
url: '/entries/new',
type: 'POST',
data: {
title: titleValue,
entry_type: typeValue,
date_created: dateValue,
description: descriptionValue
        }, success: function(data) {
	    if(data.key = 1){
                displayError();
                return;
           }
            console.log("The Post Script has finished");
		location.reload(); 
       }
    });

//this doesnt work idk
//$('#createEntryModal').modal('hide');

//formats the date into YYYY-MM-DD
    function formatDate(date) {
        var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    }

   // location.reload();
}

