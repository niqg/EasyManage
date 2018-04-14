function onSignIn(googleUser)
{
    var SUCCESS_KEY = 0;
    var ERROR_KEY = 1;
    var WARNING_KEY = 2;

    var profile = googleUser.getBasicProfile();
    var theUserEmail = profile.getEmail();
    console.log(theUserEmail);


    $.ajax({url:"/users/get", type: "GET", data: {userEmail: theUserEmail}, success: function(data) {
        //console.log(data.key);
        if(data.key == SUCCESS_KEY) //user exists
        {
            var googleToken = "tempID";
            //Hijacked, LOL
            $.ajax({url:"/login", type: "POST", data: {google_client_id: googleToken, email:theUserEmail}, success: function(data) {//This line of code
            window.location = "/home";
            }});
        }
        else                        //prompt user to make an account
        {
            var orgName = window.prompt("What do you want to name your organization?","defaultOrgName");
            
            while(orgName == null || orgName == "" || orgName == "defaultOrgName")
            {
                orgName = window.prompt("What do you want to name your organization?","defaultOrgName");
            }
            
            $.ajax({url:"/users/new", type: "POST", data: {userEmail: theUserEmail, userType:"ORG", org_Name:orgName}, success: function(data) {}});
            
            
            $.ajax({url:"/login", type: "POST", data: {google_client_id: googleToken, email:theUserEmail}, success: function(data) {
            window.location = "/home";
            }});
            
            //var modal = document.getElementById("loginModule");
            //modal.innerhtml = "";
        
        }
    }});
    

    //var profile=googleUser.getBasicProfile();
    //$(".g-signin2").css("display", "none");
    //$(".data").css("display","block");
    //$("#pic").attr('src',profile.getImageUrl());
    //$("#email").text(profile.getEmail());
    //window.location.replace("templates/userPage.html");

}


