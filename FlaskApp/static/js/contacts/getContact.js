function getContact(contactID){
	$.ajax({
	url: '/contacts/view',
	type: 'GET',
	data: {
	contact_id: contactID,
        },
	success: function(data) {
            console.log("The Post Contact Script has finished");
	    var emails = data.emails;
            var addresses = data.addresses;
	    var phoneNumbers = data.phone_numbers;
	    contact = [emails, addresses, phoneNumbers];
	    console.log(emails);
	    console.log(addresses);
	    console.log(phoneNumbers);
	    console.log(contact);
	 
	 }
    });
}
