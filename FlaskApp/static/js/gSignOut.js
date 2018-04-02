function googleSignOut()
{
    //$('#logout').click(function() {
    $.getJSON("/logout", {},
    function(data) {
        window.location = "/index";
    });
    //return false;
    //});
}
