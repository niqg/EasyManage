function onSignIn(googleUser)
{
    var SUCCESS_KEY = 0;
    var ERROR_KEY = 1;
    var WARNING_KEY = 2;

    var profile = googleUser.getBasicProfile();
    var theUserEmail = profile.getEmail();
    console.log(theUserEmail);
    
    var googleToken = theUserEmail;//googleUser.getId();// should be changed to be verified by backend at some point. https://developers.google.com/identity/sign-in/web/backend-auth
    
    
    //Hijacked, LOL
    $.ajax({url:"/login", type: "POST", data: {google_client_id: googleToken, email:theUserEmail}, success: function(data) {//Login if i can
        console.log(data.key);
        if(data.key == SUCCESS_KEY)
        {        
            window.location = "/home";    //login successful
        }
        else                              //prompt user to create an account. 
        {
            var orgName = window.prompt("What do you want to name your organization?","defaultOrgName");
            
            while(orgName == "" || orgName == "defaultOrgName")                        //make sure they give us good information. 
            {
                alert("Please Enter a valid organization Name.");
                orgName = window.prompt("What do you want to name your organization?","defaultOrgName");
            }
            
            if(orgName != null)    //orgName is null if they pressed cancel // not null if they pressed okay. 
            { 
                //create account
                $.ajax({url:"/account/new", type: "POST", data: {google_client_id: googleToken, userEmail: theUserEmail, userType:"ORG", org_name:orgName}, success: function(data) {}});
                //navigate to home page. 
                $.ajax({url:"/login", type: "POST", data: {google_client_id: googleToken, email:theUserEmail}, success: function(data) {
                    window.location = "/home";
                }});
            }//else they pressed cancel - refresh the page.         
        }
    }});    
}    
    
/*

    $.ajax({url:"/users/get", type: "GET", data: {userEmail: theUserEmail}, success: function(data) {
        //console.log(data.key);
        if(data.key == SUCCESS_KEY) //user exists
        {

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
    }});*/
    

    //var profile=googleUser.getBasicProfile();
    //$(".g-signin2").css("display", "none");
    //$(".data").css("display","block");
    //$("#pic").attr('src',profile.getImageUrl());
    //$("#email").text(profile.getEmail());
    //window.location.replace("templates/userPage.html");


