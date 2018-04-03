function putEntry() {

    console.log("Post Entry Script has been fired");

//our modal that contains the form we fill out
    var titleField = document.getElementById("modifyEntryTitle");
    var descriptionField = document.getElementById("modifyEntryDescription");
    var entryID = document.getElementById("modifyEntryID").value;
    var sendingData={entry_id: entryID};
    if(titleField.value != titleField.defaultValue) sendingData.title = titleField.value;
    if(descriptionField.value != descriptionField.defaultValue) sendingData.description = descriptionField.value;
    
//Different post
    $.ajax({
url: '/entries/modify',
type: 'PUT',
data: $.param(sendingData),
success: function(data) {
            console.log("The Put Script has finished");
        }
    });
}

