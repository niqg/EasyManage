function markComplete(){
	console.log("The Mark Complete script has fired");
	var entryID = document.getElementById("modentryIDInput").value;
	console.log("ENTRY ID: " + entryID);
	var sendingData={entry_id: entryID};
	sendingData.status = 'Completed';
	

    
	$.ajax({
	url: '/entries/modify',
	type: 'PUT',
	data: $.param(sendingData),
	success: function(data) {
	            console.log("The Mark Complete Script has finished");
	        }   location.reload();
	    });
    
}
