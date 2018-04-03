function deleteEntry() {
var entryID = document.getElementById("modifyEntryID").value;
console.log(entryID);

$.ajax({
url: "/entries/remove",
type: "DELETE",
data: {entry_id: entryID},
success: function(data) {
console.log(data);
}});
location.reload();
}
