function displayError(){
	var alert = document.getElementById("permAlert");
    if (alert.style.display === "none") {
        alert.style.display = "block";
    } 
}

function hideError(){
	var alert = document.getElementById("permAlert");
	alert.style.display = "none";
}
