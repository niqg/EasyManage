function getCal(){
setState("Calendar");
toggleCalendar();
var panel = document.getElementById("panelHeader");
setState("Calendar");
var header = document.getElementById("entryHeader");
header.innerHTML = "Calendar";
var table = document.getElementById("tableid");
table.innerHTML = "";
$(document).ready(function() {

    $('#calendar').fullCalendar({

      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,listYear'
      },

      displayEventTime: false, // don't show the time column in list view

      // THIS KEY WON'T WORK IN PRODUCTION!!!
      // To make your own Google API key, follow the directions here:
      // http://fullcalendar.io/docs/google_calendar/
      googleCalendarApiKey: 'AIzaSyDcnW6WejpTOCffshGDDb4neIrXVUA1EAE',

      // US Holidays
      events: 'en.usa#holiday@group.v.calendar.google.com',

      eventClick: function(event) {
        // opens events in a popup window
       window.open(event.url, 'gcalevent');
        return false;
      },

      loading: function(bool) {
        $('#loading').toggle(bool);
      }

    });

  });
}
