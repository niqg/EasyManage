function populatePurchaseOrdersModalData(entryid, tle, dte, sts, prc_cost, desc){
	 var entryID  = document.getElementById("modifyEntryID");
	 var title  = document.getElementById("modifyEntryTitle");
	 var date =  document.getElementById("modifyEntryDate");
	 var type =  document.getElementById("modifyEntryType");
	 var description  = document.getElementById("modifyEntryDescription");
	 entryID.value = entryid;
	 title.value = tle;
	 date.value = dte;
	 type.value = prc_cost;
	 description.value = desc;
}
