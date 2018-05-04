function populateModifyEntryModal(entryIDInp, titleInp, typeInp, dateCreatedInp, statusInp, dateCompletedInp,
								costInp, descriptionInp){
	var entryID = entryIDInp;
	//var fake = fakeInp;
	var title = titleInp;
	var type = typeInp;
	var dateCreated = dateCreatedInp;
	var status = statusInp;
	var dateCompleted = dateCompletedInp;
	var cost = costInp;
	var description = descriptionInp;
	console.log(descriptionInp + "asdf");
	var panelBody = document.getElementById("modifyEntryModalBody");
	panelBody.innerHTML = "";
	var panelFooter = document.getElementById("modifyEntryModalFooter");	
//	panelFooter.innerHTML = "";
	var entryIDDiv = document.createElement("div");
	var entryIDDiv1 = document.createElement("div");
	var entryIDLabel = document.createElement("label");
	entryIDLabel.innerHTML = "You are now modifying an Entry";
	//entryIDLabel.setAttribute("style", "visibility: hidden");
	var entryIDInput = document.createElement("input");
	entryIDInput.value = entryID;
	entryIDInput.setAttribute("style", "visibility: hidden");
	//entryIDInput.setAttribute("style", "visibility: hidden");
	entryIDInput.id = "modentryIDInput";
	//fakeDiv = document.createElement("div");
	//fakeEntryInput = document.createElement("input");
	//fakeEntryInput.disabled = true;
	//fakeEntryInput.id = "fakeEntryId";
	//fakeEntryInput.value = fake;
	//fakeDiv.appendChild(fakeEntryInput);
	entryIDDiv.appendChild(entryIDLabel);
	entryIDDiv1.appendChild(entryIDInput);
	//entryIDDiv1.appendChild(fakeDiv);
	
	var titleDiv = document.createElement("div");
	var titleDiv1 = document.createElement("div");
	var titleLabel = document.createElement("label");
	titleLabel.innerHTML = "Title";
	var titleInput = document.createElement("input");
	titleInput.value = title;
	//titleInput.disabled = true;
	titleInput.id = "modtitleInput";
	titleDiv.appendChild(titleLabel);
	titleDiv1.appendChild(titleInput);
	
	var typeDiv = document.createElement("div");
	var typeDiv1 = document.createElement("div");
	var typeLabel = document.createElement("label");
	typeLabel.innerHTML = "Type";
	var typeInput = document.createElement("input");
	typeInput.value = type;
	typeInput.disabled = true;
	typeInput.id = "modtypeInputID";
	typeDiv.appendChild(typeLabel);
	typeDiv1.appendChild(typeInput);
	
	var dateCreatedDiv = document.createElement("div");
	var dateCreatedDiv1 = document.createElement("div");
	var dateCreatedLabel = document.createElement("label");
	dateCreatedLabel.innerHTML = "Date Created";
	var dateCreatedInput = document.createElement("input");
	dateCreatedInput.value = dateCreated;
	dateCreatedInput.disabled = true;
	dateCreatedInput.id = "moddateCreatedInput";
	dateCreatedDiv.appendChild(dateCreatedLabel);
	dateCreatedDiv1.appendChild(dateCreatedInput);
	
	var statusDiv = document.createElement("div");
	var statusDiv1 = document.createElement("div");
	var statusLabel = document.createElement("label");
	statusLabel.innerHTML = "Status";
	var statusInput = document.createElement("input");
	statusInput.value = status;
	statusInput.disabled = true;
	statusInput.id = "modstatusInputID";
	statusDiv.appendChild(statusLabel);
	statusDiv1.appendChild(statusInput);
	
	var dateCompletedDiv = document.createElement("div");
	var dateCompletedDiv1 = document.createElement("div");
	var dateCompletedLabel = document.createElement("label");
	dateCompletedLabel.innerHTML = "Date Completed Yadayada";
	var dateCompletedInput = document.createElement("input");
	dateCompletedInput.value = dateCompleted;
	dateCompletedInput.disabled = true;
	dateCompletedInput.id = "moddateCompletedInput";
	//dateCompletedDiv.appendChild(dateCompletedLabel);
	//dateCompletedDiv1.appendChild(dateCompletedInput);
	
	var costDiv = document.createElement("div");
	var costDiv1 = document.createElement("div");
	var costLabel = document.createElement("label");
	costLabel.innerHTML = "Cost";
	var costInput = document.createElement("input");
	costInput.value = cost;
	//costInput.disabled = true;
	costInput.id = "modcostInput";
	costDiv.appendChild(costLabel);
	costDiv1.appendChild(costInput);
	
	var descriptionDiv = document.createElement("div");
	var descriptionDiv1 = document.createElement("div");
	var descriptionLabel = document.createElement("label");
	descriptionLabel.innerHTML = "description";
	var descriptionInput = document.createElement("textarea");
	descriptionInput.rows = "3";
	descriptionInput.setAttribute("style", "width: 500px");
	descriptionInput.innerHTML = description;
	//descriptionInput.disabled = true;
	descriptionInput.id = "moddescriptionInput";
	descriptionDiv.appendChild(descriptionLabel);
	descriptionDiv1.appendChild(descriptionInput);
	
	
	entryIDDiv.style.padding = "10px 10px 10px 0px";
	titleDiv.style.padding = "10px 10px 10px 0px";
	typeDiv.style.padding = "10px 10px 10px 0px";
	dateCreatedDiv.style.padding = "10px 10px 10px 0px";
	statusDiv.style.padding = "10px 10px 10px 0px";
	dateCompletedDiv.style.padding = "10px 10px 10px 0px";
	costDiv.style.padding = "10px 10px 10px 0px";
	descriptionDiv.style.padding = "10px 10px 10px 0px";

	panelBody.appendChild(entryIDDiv);
	panelBody.appendChild(entryIDDiv1);
	
	panelBody.appendChild(titleDiv);
	panelBody.appendChild(titleDiv1);
	
	if(type != "N/A"){
	panelBody.appendChild(typeDiv);
	panelBody.appendChild(typeDiv1);
	}
	
	if(dateCreated != "N/A"){
	panelBody.appendChild(dateCreatedDiv);
	panelBody.appendChild(dateCreatedDiv1);
	}
	
	if(status != "N/A"){
	panelBody.appendChild(statusDiv);
	panelBody.appendChild(statusDiv1);
	}
	
	//if(dateCompleted != "N/A"){
	//panelBody.appendChild(dateCompletedDiv);
	//panelBody.appendChild(dateCompletedDiv1);
	//}
	
	//if(cost != "N/A"){
	//panelBody.appendChild(costDiv);
	//panelBody.appendChild(costDiv1);
	//}
	
	panelBody.appendChild(descriptionDiv);
	panelBody.appendChild(descriptionDiv1);
	
	var editButton = document.createElement("button");
	//editButton.addEventListener("click", enableButtons());
	editButton.innerHTML = "Edit";
	var saveButton = document.createElement("button");
    	//saveButton.addEventListener("click", putEntry());
	saveButton.innerHTML = "Save";
	//panelFooter.appendChild(editButton);
	//panelFooter.appendChild(saveButton);

	function enableModifyInputs(){
		entryIDInput.disabled = false;
		titleInput.disabled = false;
		typeInput.disabled = false;
		dateCreatedInput.disabled = false;
		statusInput.disabled = false;
		dateCompletedInput.disabled = false;
		costInput.disabled = false;
		descriptionInput.disabled = false;
	}

	function disableModifyInputs(){
        entryIDInput.disabled = true;
        titleInput.disabled = true;
        typeInput.disabled = true;
        dateCreatedInput.disabled = true;
        statusInput.disabled = true;
        dateCompletedInput.disabled = true;
        costInput.disabled = true;
        descriptionInput.disabled = true;
        }
}
