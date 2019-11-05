$(function () {

    let buttonpressed;
    let interval_var;
    // Submit post on submit
    $('.submitbutton').click(function () {
        buttonpressed = $(this).attr('name')
    });
    $('#SimulatorForm').on('submit', function (event) {
        event.preventDefault();
        if (buttonpressed == "Continuous") {
            console.log("Continuous Submission button was pressed.");
            create_post();
            interval_var = setInterval(create_post, 5000);
        } else if (buttonpressed == "Once") {
            console.log("Submit Once button was pressed.");
            if (interval_var) {
                clearInterval(interval_var);
            }
            create_post();
        } else if (buttonpressed == "Stop") {
            console.log("Stopping continuous submission.");
            if (interval_var) {
                clearInterval(interval_var);
            }
        }
    });

    // AJAX for posting
    function create_post() {
        console.log("Entered create_post() function."); // sanity check
        $.ajax({
            url: "", // the endpoint
            type: "POST", // http method
            data: {
                name: $('#post-name').val(),
                owner: $('#post-owner').val(),
                temperature: $('#post-temperature').val(),
                acceleration_x: $('#post-acceleration-X').val(),
                acceleration_y: $('#post-acceleration-Y').val(),
                acceleration_z: $('#post-acceleration-Z').val(),
                wheel_speed_fr: $('#post-wheel-speed-fr').val(),
                wheel_speed_fl: $('#post-wheel-speed-fl').val(),
                wheel_speed_br: $('#post-wheel-speed-br').val(),
                wheel_speed_bl: $('#post-wheel-speed-bl').val(),
                suspension_fr: $('#post-suspension-fr').val(),
                suspension_fl: $('#post-suspension-fl').val(),
                suspension_br: $('#post-suspension-br').val(),
                suspension_bl: $('#post-suspension-bl').val(),
                initial_fuel: $('#post-initial-fuel').val(),
                fuel_decrease_rate: $('#post-fuel-decrease-rate').val(),
                initial_oil: $('#post-initial-oil').val(),
                oil_decrease_rate: $('#post-oil-decrease-rate').val(),
                created_at: $('#post-created-at').val()
            }, // data sent with the post request

            // handle a successful response
            success: function () {
                generateValues();
                console.log("POSTing was successful."); // another sanity check
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

    }

    // Processes the form data and assigns the value to corresponding fields in the UI
    function generateValues() {
        /* This function produces a datetime timestamp for _now_ in the format of
        "YYYY-MM-DD HH:MM:SS" */
        let date = new Date();
        const yyyy = date.getFullYear();
        let dd = date.getDate();
        let mm = (date.getMonth() + 1);
        dd = ("0" + dd).slice(-2)
        mm = ("0" + mm).slice(-2)
        const cur_date = yyyy + "-" + mm + "-" + dd;
        let hours = date.getHours()
        let minutes = date.getMinutes()
        let seconds = date.getSeconds();
        hours = ("0" + hours).slice(-2);
        minutes = ("0" + minutes).slice(-2);
        seconds = ("0" + seconds).slice(-2);
        const cur_time = hours + ":" + minutes + ":" + seconds;
        var dateTime = cur_date + " " + cur_time;
        
        var random_int = Math.ceil(Math.random() * 4);
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
        $("#post-created-at").val(dateTime);
        $('#post-temperature').val(temperature + random_int);
        $('#post-acceleration-X').val(acceleration_x + random_int);
        $('#post-acceleration-Y').val(acceleration_y + random_int);
        $('#post-acceleration-Z').val(acceleration_z + random_int);
        $('#post-wheel-speed-fr').val(wheel_speed_fr + random_int);
        $('#post-wheel-speed-fl').val(wheel_speed_fl + random_int);
        $('#post-wheel-speed-br').val(wheel_speed_br + random_int);
        $('#post-wheel-speed-bl').val(wheel_speed_bl + random_int);
        $('#post-suspension-fr').val(suspension_fr + random_int);
        $('#post-suspension-fl').val(suspension_fl + random_int);
        $('#post-suspension-br').val(suspension_br + random_int);
        $('#post-suspension-bl').val(suspension_bl + random_int);
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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});
