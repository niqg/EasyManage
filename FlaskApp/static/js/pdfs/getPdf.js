function getPdfs(){
	var pdfs = document.getElementById("displayPdfs");
	pdfs.innerHTML = "";
	var modal = document.getElementById("addPdfModalBody");
	var entryId = document.getElementById("modentryIDInput").value;	
	console.log("ENTRY ID: + "+ entryId);
	$.ajax({
	url: '/entries/pdf',
	type: 'GET',
	data: {entry_id : entryId},
	success: function(data) {
	        console.log("The PDF Getter Script has fire");
		if (data.key === 1){
			var label = document.createElement("label");
			label.innerHTML = "No file currently attached";
			pdfs.appendChild(label);
			return;	
		}
	        console.log(data.data);
		var labelTitle = document.createElement("label");
                labelTitle.innerHTML = "Attached Files";
		pdfs.appendChild(labelTitle);
		console.log("DATA LENTH: " + data.data.length);
		for (i = 0; i < data.data.length; i++) { 
			var div = document.createElement("div");
			var pdfId = data.data[i][0];
                	var pdfName = data.data[i][1];
                	var label = document.createElement("button");
                	label.innerHTML = pdfName;
                	label.addEventListener("click", function(){
                    	viewPdf(pdfId);
                	});
			div.appendChild(label);
			pdfs.appendChild(div);

	        }
	      }
	    });

}
