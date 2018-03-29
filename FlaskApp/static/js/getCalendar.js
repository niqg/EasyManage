function getCalendar() {
    var Table = document.getElementById("tableid");
    Table.innerHTML = "";
    var contentHeader = document.getElementById("entryHeader");
    var date = document.getElementById("calendarDate");
    date.style.display = "table";
    contentHeader.innerHTML = "Calendar";
    console.log("Calendar Script has been fired");
}
