function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
  // Submit post on submit
  function create_register(){
    console.log("create post is working!"); // sanity check
    $.ajax({
      url : "/register", // the endpoint
      type : "POST", // http method
      data : {
        username : $('#id_username').val(),
        password : $('#id_password').val(),
        email : $('#id_email').val(),
      }, // data sent with the post request
      // handle a successful response
      success: function(json) {
          console.log('successful');
          $('#post-text').val(''); // remove the value from the input
          message = JSON.parse(json) // another sanity check
          console.log(message['results']);
          $('#results').html("<div class='alert-box alert radius' data-alert>"+ message +
              " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      },
      // handle a non-successful response
      error: function(xhr,errmsg,err) {
        message = JSON.parse(xhr.responseText)['error']
          $('#results').html("<div class='alert-box alert radius' data-alert>"+ message +
              " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      }
    });
  };

  $('#post-form').on('submit', function(event){
      event.preventDefault();
      console.log("form submitted!");  // sanity check
      create_register();
  });

