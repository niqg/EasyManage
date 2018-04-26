function putEntry() {

    console.log("Post Entry Script has been fired");

	//our modal that contains the form we fill out
    var titleField = document.getElementById("modtitleInput");
    var descriptionField = document.getElementById("moddescriptionInput");
    var entryID = document.getElementById("modentryIDInput").value;
    var sendingData={entry_id: entryID};
    console.log(titleField.value);
    console.log(descriptionField.value);
    console.log(entryID.value);
    if(titleField.value != titleField.defaultValue) sendingData.title = titleField.value;
    if(descriptionField.value != descriptionField.defaultValue) sendingData.description = descriptionField.value;
  /*  if(document.getElementById("modtypeInputID") != null){
	var type = document.getElementById("modtypeInputID");
	sendingData.d_type = type.value;
    }
    if(document.getElementById("moddateCreatedInput") != null){
        var date = document.getElementById("moddateCreatedInput");
        sendingData.date_created = date.value;
    }
    if(document.getElementById("modstatusInputID") != null){
        var statusOf = document.getElementById("modstatusInputID");
        sendingData.status = statusOf.value;
    }
    if(document.getElementById("moddateCompletedInput") != null){
        var date = document.getElementById("moddateCompletedInput");
        sendingData.completion_date = date.value;
    } */
   // if(document.getElementById("modcostInput").value != null){
      //  var costOf = document.getElementById("modcostInput");
      //  sendingData.purchase_col = costOf.value;
   // } 
//	console.log(costOf.value);
	//Different post
 	   $.ajax({
	url: '/entries/modify',
	type: 'PUT',
	data: $.param(sendingData),
	success: function(data) {
	   	    if(data.key === 1){
			displayError();
			return;
		    }
	            console.log("The Put Script has finished");
		    location.reload();
	        }
	    });
	}
