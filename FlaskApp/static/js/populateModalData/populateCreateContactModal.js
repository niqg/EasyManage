function populateCreateContactModal(){
	var panelBody = document.getElementById("createContactModalBody");
	var panelFooter = document.getElementById("createContactModalFooter");
	panelBody.innerHTML = "";
	var titleDiv = document.createElement("div");
	var titleDiv1 = document.createElement("div");
	var titleLabel = document.createElement("label");
	titleLabel.innerHTML = "Name";
	var titleInput = document.createElement("input");
	titleInput.id = "titleInputID";
	titleDiv.appendChild(titleLabel);
	titleDiv1.appendChild(titleInput);
	
	var companyDiv = document.createElement("div");
	var companyDiv1 = document.createElement("div");
	var companyLabel = document.createElement("label");
	companyLabel.innerHTML = "Company";
	var companyInput = document.createElement("input");
	companyInput.id = "companyInputID";
	companyDiv.appendChild(companyLabel);
	companyDiv1.appendChild(companyInput);

	var dtypeDiv = document.createElement("div");
	var dtypeDiv1 = document.createElement("div");
	var dtypeLabel = document.createElement("label");
	dtypeLabel.innerHTML = "Contact Type";
	dtypeDropdown = document.createElement("select");
	dtypeDropdown.id = "dtypeInputID";
	var op1 = new Option();
	op1.value = "SPP";
	op1.text = "Supplier";
	dtypeDropdown.options.add(op1);
	var op2 = new Option();
        op2.value = "CNT";
        op2.text = "Contractor";
        dtypeDropdown.options.add(op2);
	var op3 = new Option();
        op3.value = "BTH";
        op3.text = "Both";
        dtypeDropdown.options.add(op3);
	dtypeDiv.appendChild(dtypeLabel);
	dtypeDiv1.appendChild(dtypeDropdown);

	numberDiv = document.createElement("div");
	numberDiv1 = document.createElement("div");
	var numberLabel = document.createElement("label");
	numberLabel.innerHTML = "Primary Number";
	var numberInput = document.createElement("input");
	numberInput.id = "primaryNumber";
	numberInput.classList.add("numberClass");
	var numberDropdown = document.createElement("select");
        numberDropdown.id = "numberDropdownInputID";
        var op1 = new Option();
        op1.value = 1;
        op1.text = "CELL";
        numberDropdown.options.add(op1);
        var op2 = new Option();
        op2.value = 2;
        op2.text = "HOME";
	numberDropdown.options.add(op2);
		
	var numberAddButton = document.createElement("button");
	numberAddButton.addEventListener("click", addSecondaryNumber, false);
	numberAddButton.innerHTML = "add secondary number";
	numberDiv.appendChild(numberLabel);
	numberDiv1.appendChild(numberInput);
	numberDiv1.appendChild(numberDropdown);
	numberDiv1.appendChild(numberAddButton);

	emailDiv = document.createElement("div");
        emailDiv1 = document.createElement("div");
        var emailLabel = document.createElement("label");
        emailLabel.innerHTML = "Primary Email";
        var emailInput = document.createElement("input");
	emailInput.id = "primaryEmail";
	emailInput.classList.add("emailClass");
        var emailAddButton = document.createElement("button");
        emailAddButton.addEventListener("click", addSecondaryEmail, false); 
        emailAddButton.innerHTML = "add secondary email";
        emailDiv.appendChild(emailLabel);
        emailDiv1.appendChild(emailInput);
        emailDiv1.appendChild(emailAddButton);

	addressDiv = document.createElement("div");
        addressDiv1 = document.createElement("div");
        var addressLabel = document.createElement("label");
        addressLabel.innerHTML = "Address";
        var addressInput = document.createElement("input");
        addressInput.id = "addressInput";
        addressInput.classList.add("addressClass");
        var addressAddButton = document.createElement("button");
        addressAddButton.addEventListener("click", addSecondaryAddress, false);
        addressAddButton.innerHTML = "add secondary address";
        addressDiv.appendChild(addressLabel);
        addressDiv1.appendChild(addressInput);
        addressDiv1.appendChild(addressAddButton);


	titleDiv.style.padding = "10px 10px 10px 0px";
	companyDiv.style.padding = "10px 10px 10px 0px";
	dtypeDiv.style.padding = "10px 10px 10px 0px";
	numberDiv.style.padding = "10px 10px 10px 0px";
	emailDiv.style.padding = "10px 10px 10px 0px";
	addressDiv.style.padding = "10px 10px 10px 0px";

	panelBody.appendChild(titleDiv);
	panelBody.appendChild(titleDiv1);
	panelBody.appendChild(companyDiv);
	panelBody.appendChild(companyDiv1);
	panelBody.appendChild(dtypeDiv);
	panelBody.appendChild(dtypeDiv1);
	panelBody.appendChild(numberDiv);
	panelBody.appendChild(numberDiv1);
	panelBody.appendChild(emailDiv);
	panelBody.appendChild(emailDiv1);
	panelBody.appendChild(addressDiv);
	panelBody.appendChild(addressDiv1);
	
	function addSecondaryNumber(){
		var numberSecondaryDiv = document.createElement("div");
		var numberSecondaryInput = document.createElement("input");
		var numberDropdown = document.createElement("select");
        	numberDropdown.id = "numberDropdownInputID";
        	var op1 = new Option();
        	op1.value = 1;
        	op1.text = "CELL";
        	numberDropdown.options.add(op1);
        	var op2 = new Option();
        	op2.value = 2;
        	op2.text = "HOME";
        	numberDropdown.options.add(op2);
		numberSecondaryInput.id = "secondaryNumber";
		numberSecondaryInput.classList.add("numberClass");
		numberSecondaryDiv.appendChild(numberSecondaryInput);
		numberSecondaryDiv.appendChild(numberDropdown);
		numberDiv1.appendChild(numberSecondaryDiv);
	}

	function addSecondaryEmail(){
                var emailSecondaryDiv = document.createElement("div");
                var emailSecondaryInput = document.createElement("input");
                emailSecondaryInput.id = "secondaryEmail";
		emailSecondaryInput.classList.add("emailClass");
                emailSecondaryDiv.appendChild(emailSecondaryInput);
                emailDiv1.appendChild(emailSecondaryDiv);
        }

	function addSecondaryAddress(){
                var addressSecondaryDiv = document.createElement("div");
                var addressSecondaryInput = document.createElement("input");
                addressSecondaryInput.id = "secondaryAddress";
                addressSecondaryInput.classList.add("addressClass");
                addressSecondaryDiv.appendChild(addressSecondaryInput);
                addressDiv1.appendChild(addressSecondaryDiv);
        }

}
