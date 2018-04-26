function deleteEntry() {
var entryID = document.getElementById("modentryIDInput").value;
console.log(entryID);

$.ajax({
url: "/entries/remove",
type: "DELETE",
data: {entry_id: entryID},
success: function(data) {
if(data.key === 1){
                displayError();
                return;
           }
console.log(data)
location.reload();
}});
//location.reload();
}
