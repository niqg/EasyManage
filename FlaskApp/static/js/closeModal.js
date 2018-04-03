function closeModal(){
var mymodal = $('#modifyEntryModal');
mymodal.toggle();
document.getElementById("modifyEntryID").value = "";
document.getElementById("modifyEntryTitle").value = "";
document.getElementById("modifyEntryDescription").value = "";
}