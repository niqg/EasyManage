function postContact() {

    console.log("Post Contact Script has been fired");

	//our modal that contains the form we fill out
    var modal = document.getElementById("createContactModal").value;
    var modalBody = document.getElementById("createContactModalBody");
    var contactId;

    var titleValue = document.getElementById("titleInputID").value;
    var companyValue = document.getElementById("companyInputID").value;
    var dtypeValue = document.getElementById("dtypeInputID").value;
    var numberTypeValue = document.getElementById("numberDropdownInputID").value;
    var numberClass = document.getElementsByClassName("numberClass");
    //var emailClass = document.getElementsByClassName("emailClass");
    //var numberDict = new Array(numberClass.length);
	//for (i = 0; i < numberClass.length; i++) {
	//	numberDict[i] = [numberClass[i].value, numberTypeValue,	1]; 
	//}
    var emailClass = document.getElementsByClassName("emailClass");
    //var emailDict = new Array(emailClass.length);
      //  for (i = 0; i < emailClass.length; i++) {
        //        emailDict[i] = [emailClass[i].value, 1];     
       // }

    var addressClass = document.getElementsByClassName("addressClass");
    //var addressDict = new Array(addressClass.length);
      //  for (i = 0; i < addressClass.length; i++) {
        //        addressDict[i] = [addressClass[i].value,"none",	"none",	1];
        //}
    //console.log(titleValue);
    //console.log(companyValue);
    //console.log(dtypeValue);
    //console.log(numberDict);
    //console.log(emailDict);
    //console.log(addressDict);

    if(titleValue === ""){
        console.log("Opps, no entry inputted");
	var errorLabel = document.createElement("label");
	errorLabel.innerHTML = "*NAME CAN NOT BE BLANK";
        errorLabel.setAttribute("style", "color: red");
	modalBody.appendChild(errorLabel)
        return
        }

    $.ajax({
	url: '/contacts/new',
	type: 'POST',
	data: {
	name: titleValue,
	company_name: companyValue,
	contact_type: dtypeValue,
        },
	success: function(data) {
	   if(data.key === 1){
		displayError();
		return;
	   }
           contactID = data.new_contact_id;
           for (i = 0; i < numberClass.length; i++) {
                $.ajax({                                                                                      //I may have messed it up a bit, but we're gonna rewrite the endpoint.
                url: '/contacts/give_access_point/phone',
                type: 'POST',
                data: {contact_id: contactID, number: numberClass[i].value, type: numberTypeValue, priority: i}
                });
           }
           for (i = 0; i < emailClass.length; i++) {
                $.ajax({                                                                                      //I may have messed it up a bit, but we're gonna rewrite the endpoint.
                url: '/contacts/give_access_point/email',
                type: 'POST',
                data: {contact_id: contactID, email:emailClass[i].value, priority: i}
                });
           }
           for (i = 0; i < addressClass.length; i++) {
                $.ajax({                                                                                      //I may have messed it up a bit, but we're gonna rewrite the endpoint.
                url: '/contacts/give_access_point/address',
                type: 'POST',
                data: {contact_id: contactID, address: addressClass[i].value, priority: i}
                });
           } console.log("The Post Contact Script has finished");
            location.reload();
           //var sendingData={contact_id: contactId};
           //sendingData.emails = emailDict;
           //sendingData.phone_numbers = numberDict;
           //sendingData.addresses = addressDict;
	   //console.log(sendingData);

        //$.ajax({                                                                                      //I may have messed it up a bit, but we're gonna rewrite the endpoint. 
        //url: '/contacts/give_access_points',
        //type: 'PUT',
        //data: {
            // contact_id: contactId,
           //  emails: emailDict,
            // phone_numbers: numberDict,
            // addresses: addressDict
        //},
        //data: $.param(sendingData),
        //success: function(data) {
//	 }
	  //  });	   

        }
    });

    
}

