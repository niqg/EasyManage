function search(){
    input = document.getElementById("search").value;
    state = getState();
  // header.innerHTML = input;
    if(state === "Entries"){
    	if(input === ""){
    	getEntries();
    	}
    	else{
    	getFilteredEntries(input);
    	}
    }
    else if(state === "Work Orders"){
    	if(input === ""){
    	getWorkOrders();
    	}
    	else{
    	getFilteredWorkOrders(input);
    	}
    }
    else if(state === "Purchase Orders"){
    	if(input === ""){
    	getPurchaseOrders();
    	}
    	else{
    	getFilteredPurchaseOrders(input);
    	}
    }
    else if(state === "General Entries"){
    	if(input === ""){
    	getGeneralInfo();
    	}
    	else{
    	getFilteredGeneralOrders(input);
    	}
    }
    else if(state === "Contacts"){
    	if(input === ""){
    	getContacts();
    	}
    	else{
    	getFilteredContacts(input);
    	}
    }
}
