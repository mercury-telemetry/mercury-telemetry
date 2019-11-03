$(function() {

    var buttonpressed;
    var interval_var
    // Submit post on submit
    $('.submitbutton').click(function() {
        buttonpressed = $(this).attr('name')
    });
    $('#SimulatorForm').on('submit', function(event){
        event.preventDefault();
        if(buttonpressed == "Continuous"){
            create_post();
            interval_var = setInterval(create_post, 5000);
        }
        else if(buttonpressed == "Once"){
            if(interval_var){
                clearInterval(interval_var);
            }
            create_post();
        }
        else if(buttonpressed == "Stop"){
            if(interval_var){
                clearInterval(interval_var);
            }
        }
    });

    // AJAX for posting
    function create_post() {
    console.log("create post is working!"); // sanity check
    $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        data : { the_name : $('#post-name').val(),
        the_owner : $('#post-owner').val(),
        the_temperature : $('#post-temperature').val(),
        the_acceleration_x : $('#post-acceleration-X').val(),
        the_acceleration_y : $('#post-acceleration-Y').val(),
        the_acceleration_z : $('#post-acceleration-Z').val(),
        the_wheel_speed_fr : $('#post-wheel-speed-fr').val(),
        the_wheel_speed_fl : $('#post-wheel-speed-fl').val(),
        the_wheel_speed_br : $('#post-wheel-speed-br').val(),
        the_wheel_speed_bl : $('#post-wheel-speed-bl').val(),
        the_suspension_fr : $('#post-suspension-fr').val(),
        the_suspension_fl : $('#post-suspension-fl').val(),
        the_suspension_br : $('#post-suspension-br').val(),
        the_suspension_bl : $('#post-suspension-bl').val(),
        the_initial_fuel : $('#post-initial-fuel').val(),
        the_fuel_decrease_rate : $('#post-fuel-decrease-rate').val(),
        the_initial_oil : $('#post-initial-oil').val(),
        the_oil_decrease_rate : $('#post-oil-decrease-rate').val(),
        the_created_at : $('#post-created-at').val()
                 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            generateValues()
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};
    // Processes the form data and assigns the value to corresponding fields in the UI
    function generateValues(){
        var random_int = Math.ceil(Math.random()*4)
        var temperature = parseInt($('#post-temperature').val());
        var acceleration_x = parseInt($('#post-acceleration-X').val());
        var acceleration_y = parseInt($('#post-acceleration-Y').val());
        var acceleration_z = parseInt($('#post-acceleration-Z').val());
        var wheel_speed_fr = parseInt($('#post-wheel-speed-fr').val());
        var wheel_speed_fl = parseInt($('#post-wheel-speed-fl').val());
        var wheel_speed_br = parseInt($('#post-wheel-speed-br').val());
        var wheel_speed_bl = parseInt($('#post-wheel-speed-bl').val());
        var suspension_fr = parseInt($('#post-suspension-fr').val());
        var suspension_fl = parseInt($('#post-suspension-fl').val());
        var suspension_br = parseInt($('#post-suspension-br').val());
        var suspension_bl = parseInt($('#post-suspension-bl').val());
        $('#post-temperature').val(temperature+random_int);
        $('#post-acceleration-X').val(acceleration_x+random_int);
        $('#post-acceleration-Y').val(acceleration_y+random_int);
        $('#post-acceleration-Z').val(acceleration_z+random_int);
        $('#post-wheel-speed-fr').val(wheel_speed_fr+random_int);
        $('#post-wheel-speed-fl').val(wheel_speed_fl+random_int);
        $('#post-wheel-speed-br').val(wheel_speed_br+random_int);
        $('#post-wheel-speed-bl').val(wheel_speed_bl+random_int);
        $('#post-suspension-fr').val(suspension_fr+random_int);
        $('#post-suspension-fl').val(suspension_fl+random_int);
        $('#post-suspension-br').val(suspension_br+random_int);
        $('#post-suspension-bl').val(suspension_bl+random_int);
    }

    // This function gets cookie with a given name
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
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    });
