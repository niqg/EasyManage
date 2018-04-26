function signUp() {


var orgNameValue = document.getElementById("createOrgainzationName").value;

var orgEmailValue = document.getElementById("createOrganizationEmail").value;
var somePerms = 1023;



    $.ajax({
url: '/users/new',
type: 'POST',
data: {
orgName: orgNameValue,
userEmail: orgEmailValue,
userType: "ORG"
        },
success: function(data) {
            console.log("The Post Script has finished");
        }
    });


}
