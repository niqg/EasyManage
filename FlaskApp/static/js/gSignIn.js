function onSignIn(googleUser)
{
    var googleToken = "tempID";
    //Hijacked, LOL
    $.ajax({url:"/login", type: "POST", data: {google_client_id: googleToken}, success: function(data) {
        console.log(data.key);
        window.location = "/home";
    }});

    //var profile=googleUser.getBasicProfile();
    //$(".g-signin2").css("display", "none");
    //$(".data").css("display","block");
    //$("#pic").attr('src',profile.getImageUrl());
    //$("#email").text(profile.getEmail());
    //window.location.replace("templates/userPage.html");
          }
