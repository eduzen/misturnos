function generateUUID() {
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
};


$(document).ready(function() {

$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').focus()
})

// page is now ready, initialize the calendar...
$('#calendar').fullCalendar({
    lang: 'es',
    weekends: false,
    aspectRatio: 1,
    minTime: '09:00',
    maxTime: '19:00',
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
        dow: [ 1, 2, 3, 4, 5 ]
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
        $.each(pacientes, function (i, item) {
            $('#patients').append($('<option>', {
                value: item.id,
                text : item.last_name + ' ' + item.name
            }));
        });
        $('#myModal').modal('show');
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
            var start = moment(start).format("YYYY-MM-DD HH:mm");
            var end = moment(end).format("YYYY-MM-DD HH:mm");
            var uuid = generateUUID();
            console.log(uuid)
            console.log(start)
            console.log(end)

            $.ajax({
                url: '/appointment',
                dataType: 'json',
                type : "POST", // http method
                data: {
                    // our hypothetical feed requires UNIX timestamps
                    id: uuid,
                    start: start,
                    end: end,
                    allDay: allDay
                },
                success: function(doc) {
                    console.log("Exito");
                    var events = [];
                    $(doc).find('event').each(function() {
                        events.push({
                            title: $(this).attr('title'),
                            start: $(this).attr('start') // will be parsed
                        });
                    });
                    callback(events);
                }
            });

        }
        calendar.fullCalendar('unselect');
    },

 });
});
