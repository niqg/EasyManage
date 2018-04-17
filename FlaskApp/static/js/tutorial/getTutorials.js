function getTutorials() {
    setState("Settings");
    toggleCalendar();
    var Table = document.getElementById("tableid");
    Table.innerHTML = "";
    var contentHeader = document.getElementById("entryHeader");
    contentHeader.innerHTML = "Tutorials";
    console.log("Tutorial Script has been fired");
}
