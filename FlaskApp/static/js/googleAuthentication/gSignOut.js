function googleSignOut()
{
     var CLIENT_ID = '69496104427-vd134aptc08qphb7gmpqd7j55mdcmjij.apps.googleusercontent.com';
      var API_KEY = 'AIzaSyB57A4LqZGLiSsYRfYLZIyBuMfY-Hbp7EA';

    //$('#logout').click(function() {
    $.getJSON("/logout", {},
    function(data) {
	//signOut();
        //gapi.auth.signOut();
        if(data.key == 0) 
            document.location.href = "https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://axolotldevelopment.com";
            //window.location = "/index";


        //window.location = "http://axolotldevelopment.com";
    });
    //return false;
    //});
}
