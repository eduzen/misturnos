$(document).ready(function() {
// page is now ready, initialize the calendar...
$('#calendar').fullCalendar({
    lang: 'es',
    weekends: false,
    googleCalendarApiKey: 'AIzaSyARIajrk27-YXMKtVHCoXqQc1fsNiqRozo',
    eventSources: [
        {
            googleCalendarId: '9qoqs850pidfgn4cmhgj3r2cbs@group.calendar.google.com'
        },
        {
            googleCalendarId: 'es.ar#holiday@group.v.calendar.google.com'
        },
    ],
    businessHours:{
        start: '10:00', // a start time (10am in this example)
        end: '18:00', // an end time (6pm in this example)
        dow: [ 1, 2, 4, 5 ]
        // days of week. an array of zero-based day of week integers (0=Sunday)
        // (Monday-Thursday in this example)
    },
    timeFormat: 'H(:mm)', // uppercase H for 24-hour clock
    defaultView: 'agendaWeek',
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,agendaDay,month',
    },
    editable: true,
    selectable: true,
    selectHelper: true,
    //dayClick: function() {
       // alert('a day has been clicked!');
    //},
    eventClick: function(calEvent, jsEvent, view) {
        console.log(calEvent);
        console.log(calEvent._id);
        //alert('Event: ' + calEvent.title);
        //alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
        //alert('View: ' + view.name);
        // change the border color just for fun
        $(this).css('border-color', 'red');
        if(confirm('Quiere borrar el turno?')) {
          $('#calendar').fullCalendar('removeEvents',calEvent._id);
        }
    },
    select: function(start, end, allDay) {
        var title = prompt('Paciente:');
        if (title) {
            var calendar = $('#calendar')
            calendar.fullCalendar('renderEvent',
                {
                    title: title,
                    start: start,
                    end: end,
                    allDay: false
                },
                true // make the event "sticsk"
            );

        }
        calendar.fullCalendar('unselect');
    },

 });
var utc = $.fullCalendar.moment.utc('2015-01-01T12:00:00');
});
