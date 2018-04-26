function toggleCalendar(){
console.log("Toggle Calendar has been fired");
var calendar = document.getElementById("calendar");
var search = document.getElementById("searchBar");
var state = getState();
console.log("current state before calendar call is " + state);
	search.style.visibility = "visible";
	calendar.style.visibility = "hidden";
        if (state == "Calendar"){
                calendar.style.visibility = "visible";
		search.style.visibility = "hidden";
        }
	if(state == "Settings" || state == "Tutorial"){
		search.style.visibility = "hidden";
	}
}
