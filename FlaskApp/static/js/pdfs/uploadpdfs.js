function uploadPDFs()
{

    //TODO set this properly somehow. 
    var entryId = document.getElementById("modentryIDInput").value;
    var entryID = entryId;

    var control = document.getElementById("my_files");

    var i = 0,
        files = control.files,
        len = files.length;
    
    
    //need to send entryID, and pdf to @application.route("/entries/pdf/add",methods=['POST'])  
    for (; i < len; i++) {
    
        var fileName = files[i].name;
        //check to see if they gave us a pdf file
        var file_type = fileName.substr(fileName.lastIndexOf('.')).toLowerCase();
        
            var fd = new FormData();
            fd.append('fname', fileName);
            fd.append('pdf', files[i]);
            fd.append("entry_id",entryID);
            
        if (file_type  === '.pdf') {//they gave us a pdf file.  
            $.ajax({url:"/entries/pdf/add", 
            type: "POST",
             data: fd ,
                 processData: false,
                  contentType: false,
                     success: function(data) {
                console.log(data.message);
                console.log(data.user_edited);
             }});
        
        }
        
        //console.log("Filename: " + files[i].name);
        //console.log("Type: " + files[i].type);
        //console.log("Size: " + files[i].size + " bytes");
    }
    
    
    

}
