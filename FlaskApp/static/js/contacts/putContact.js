function putContact(){

	var contactID = document.getElementById("contactIdInputID");
	var name = document.getElementById("nameInputID");
	var company = document.getElementById("companyInputID");
	var primNumber = document.getElementById("numberInputID");
	var primEmail = document.getElementById("emailInputID");
	var primAddress = document.getElementById("addressInputID");

	
	$.ajax({
        url: '/contacts/modify',
        type: 'PUT',
        data: {
        contact_id: contactID.value,
        name: name.value,
        company_name: company.value,
        },
        success: function(data) {
        	console.log("The Put contact script was a success!");
            
            }
        });
        
    $.ajax({
        url: '/contacts/give_access_point/phone',
        type: 'POST',
        data: {
        contact_id: contactID.value,
        number: primNumber.value,
        type: "CELL",
        priority: 1,
        },
        success: function(data) {
		if(data.key === 1){
		   displayError();
		   return;
		}
        	console.log("The Put contact Phone script was a success!");
            
            }
        });
        
    $.ajax({
        url: '/contacts/give_access_point/address',
        type: 'POST',
        data: {
        contact_id: contactID.value,
        address: primAddress.value,
        zipcode: "",
        city: "",
        priority: 1,
        },
        success: function(data) {
        	console.log("The Put contact Address script was a success!");
            
            }
        });
        
    $.ajax({
        url: '/contacts/give_access_point/email',
        type: 'POST',
        data: {
        contact_id: contactID.value,
        email: primEmail.value,
        priority: 1,
        },
        success: function(data) {
        	console.log("The Put contact Emai; script was a success!");
            
            }
        });
        
}
