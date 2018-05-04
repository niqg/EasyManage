function populateModifyContactModal(contactIdInp, typeInp){

	var contactId = contactIdInp;	
	var type = typeInp;
	var panelBody = document.getElementById("modifyContactModalBody");
	panelBody.innerHTML = "";
    var panelFooter = document.getElementById("modifyContactModalFooter");
	//panelFooter.innerHTML = "";

        $.ajax({
        url: '/contacts/view',
        type: 'GET',
        data: {
        contact_id: contactId,
        },
        success: function(data) {
            console.log("The Post Contact Script has finished");
            var emails = data.emails;
            var addresses = data.addresses;
            var phoneNumbers = data.phone_numbers;
            var info = data.info;
            
    //var number = numberInp;
	//var email = emailInp;
	

	var contactIdDiv = document.createElement("div");
    var contactIdDiv1 = document.createElement("div");
    var contactIdLabel = document.createElement("label");
    contactIdLabel.innerHTML = "You are now modifying a Contact";
    var contactIdInput = document.createElement("input");
    contactIdInput.value = contactId;
    contactIdInput.disabled = true;
    contactIdInput.setAttribute("style", "visibility: hidden");
    contactIdInput.id = "contactIdInputID";
    contactIdDiv.appendChild(contactIdLabel);
    contactIdDiv1.appendChild(contactIdInput);


	var nameDiv = document.createElement("div");
	var nameDiv1 = document.createElement("div");
	var nameLabel = document.createElement("label");
	nameLabel.innerHTML = "Name";
	var nameInput = document.createElement("input");
	nameInput.value = info[1];
	//nameInput.disabled = true;
	nameInput.id = "nameInputID";
	nameDiv.appendChild(nameLabel);
	nameDiv1.appendChild(nameInput);
	
	var companyDiv = document.createElement("div");
	var companyDiv1 = document.createElement("div");
	var companyLabel = document.createElement("label");
	companyLabel.innerHTML = "Company";
	var companyInput = document.createElement("input");
	companyInput.value = info[2];
	//companyInput.disabled = true;
	companyInput.id = "companyInputID";
	companyDiv.appendChild(companyLabel);
	companyDiv1.appendChild(companyInput);
	
	var typeDiv = document.createElement("div");
	var typeDiv1 = document.createElement("div");
	var typeLabel = document.createElement("label");
	typeLabel.innerHTML = "Type";
	var typeInput = document.createElement("input");
	typeInput.value = type;
	typeInput.disabled = true;
	typeInput.id = "typeInputID";
	typeDiv.appendChild(typeLabel);
	typeDiv1.appendChild(typeInput);
	
	var numberDiv = document.createElement("div");
	var numberDiv1 = document.createElement("div");
	var numberLabel = document.createElement("label");
	numberLabel.innerHTML = "Number";
	var numberInput = document.createElement("input");
	numberInput.placeholder= 'New Number...';
	//numberInput.disabled = true;
	numberInput.id = "numberInputID";
	numberDiv.appendChild(numberLabel);
	numberDiv1.appendChild(numberInput);
	
	var emailDiv = document.createElement("div");
	var emailDiv1 = document.createElement("div");
	var emailLabel = document.createElement("label");
	emailLabel.innerHTML = "Email";
	var emailInput = document.createElement("input");
	emailInput.placeholder= 'New Email...';
	//emailInput.disabled = true;
	emailInput.id = "emailInputID";
	emailDiv.appendChild(emailLabel);
	emailDiv1.appendChild(emailInput);
	
	var addressDiv = document.createElement("div");
	var addressDiv1 = document.createElement("div");
	var addressLabel = document.createElement("label");
	addressLabel.innerHTML = "Address";
	var addressInput = document.createElement("input");
	addressInput.placeholder= 'New Address...';
	//addressInput.disabled = true;
	addressInput.id = "addressInputID";
	addressDiv.appendChild(addressLabel);
	addressDiv1.appendChild(addressInput);
	
	
	nameDiv.style.padding = "10px 10px 10px 0px";
	companyDiv.style.padding = "10px 10px 10px 0px";
	typeDiv.style.padding = "10px 10px 10px 0px";
	numberDiv.style.padding = "10px 10px 10px 0px";
	emailDiv.style.padding = "10px 10px 10px 0px";

	panelBody.appendChild(contactIdDiv);
	panelBody.appendChild(contactIdDiv1);
	panelBody.appendChild(nameDiv);
	panelBody.appendChild(nameDiv1);
	panelBody.appendChild(companyDiv);
	panelBody.appendChild(companyDiv1);
	panelBody.appendChild(typeDiv);
	panelBody.appendChild(typeDiv1);
	panelBody.appendChild(numberDiv);
	//populateSecondaryNumber();
	panelBody.appendChild(numberDiv1);
	panelBody.appendChild(emailDiv);
	panelBody.appendChild(emailDiv1);
	panelBody.appendChild(addressDiv);
	panelBody.appendChild(addressDiv1);
	
	
	
	//populateSecondaryNumber();
	//populateSecondaryEmail();
	//populateSecondaryAddress();
	
	if(addresses[0] != null){
			console.log("Secondary Address Script has Fired");
			populateSecondaryAddress();
	
	}
	
	if(phoneNumbers[0] != null){
			console.log("Secondary number Script has Fired");
			populateSecondaryNumber();
        }
        
	if(emails[0] != null){
			console.log("Secondary email Script has Fired");
			populateSecondaryEmail();
        }
	
	
	function populateSecondaryNumber(){
                for(i = 0; i < phoneNumbers.length; i++){
				var secnumberDiv = document.createElement("div");
                var secnumberDiv1 = document.createElement("div");
                var secnumberInput = document.createElement("input");
                secnumberInput.value = phoneNumbers[i][1];
                //secaddressInput.disabled = true;
                secnumberInput.id = "secnumberInputID" + i;
                numberDiv1.appendChild(secnumberInput);
                //var deleteButton = document.createElement("button");
                //deleteButton.innerHTML = "remove";
                //secaddressDiv.appendChild(secaddressLabel);
                //numberDiv1.appendChild(secnumberInput);
                //secaddressDiv1.appendChild(deleteButton);
                //panelBody.appendChild(secnumberDiv);
                //panelBody.appendChild(secnumberDiv1);
                }

        
	   }
	   
	   function populateSecondaryEmail(){
			//var secaddressLabel = document.createElement("label");
              //  secaddressLabel.innerHTML = "Secondary Address";
                for(i = 0; i < emails.length; i++){
				var secemailDiv = document.createElement("div");
                var secemailDiv1 = document.createElement("div");
                var secemailInput = document.createElement("input");
                //console.log("email i-1" + emails[i][1]);
                secemailInput.value = emails[i][1];
                //secemailInput.disabled = true;
                emailDiv1.appendChild(secemailInput);
                secemailInput.id = "secemailInputID" + i;
                //var deleteButton = document.createElement("button");
                //deleteButton.innerHTML = "remove";
                //secaddressDiv.appendChild(secaddressLabel);
                //secaddressDiv1.appendChild(deleteButton);
                //panelBody.appendChild(secemailDiv);
                //panelBody.appendChild(secemailDiv1);
                }
		}
	   
	function populateSecondaryAddress(){
			//var secaddressLabel = document.createElement("label");
               // secaddressLabel.innerHTML = "Secondary Address";
                for(i = 0; i < addresses.length; i++){
				//var secaddressDiv = document.createElement("div");
                //var secaddressDiv1 = document.createElement("div");
                var secaddressInput = document.createElement("input");
                secaddressInput.value = addresses[i][1];
                //secaddressInput.disabled = true;
                secaddressInput.id = "secaddressInputID" +i;
                var deleteButton = document.createElement("button");
                deleteButton.innerHTML = "remove";
                //secaddressDiv.appendChild(secaddressLabel);
                addressDiv1.appendChild(secaddressInput);
                //secaddressDiv1.appendChild(deleteButton);
                //panelBody.appendChild(secaddressDiv);
                //panelBody.appendChild(secaddressDiv1);
                }
		}
	   

                        
	}
	});
}
	

