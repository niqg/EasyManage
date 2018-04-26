function toggleModifyButtons(){
	buttonGroup = document.getElementById("modifyButtonGroup");
	editButton = document.getElementById("editButton");
	if ( buttonGroup.style.visibility='visible'){
		editButton.style.visibility='hidden';
	}
	if(editButton.style.visibility='visible'){
		buttonGroup.style.visibility='visible';
	}
	

}