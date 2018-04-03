function populateWorkOrdersModalData(entryid, tle, dte, sts, dte_comp, desc){
	 var entryID  = document.getElementById("modifyEntryID");
	 var title  = document.getElementById("modifyEntryTitle");
	 var date =  document.getElementById("modifyEntryDate");
	 var type =  document.getElementById("modifyEntryType");
	 var description  = document.getElementById("modifyEntryDescription");
	 entryID.value = entryid;
	 title.value = tle;
	 date.value = dte;
	 type = "date complete";
	 type.value = dte_comp;
	 description.value = desc;
}