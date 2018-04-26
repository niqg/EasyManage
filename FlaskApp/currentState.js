var state = "";

function setState(stateInput){
	var table = document.getElementById("tableid");
	state = stateInput;
        console.log("The state has been changed to " +  stateInput);
}

function getState(){
	return state;
}
