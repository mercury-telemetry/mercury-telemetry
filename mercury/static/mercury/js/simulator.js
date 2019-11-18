$(function () {

    let buttonpressed;
    let interval_var;
    let button_counter=0;
    // Submit post on submit
    $('.submitbutton').click(function () {
        buttonpressed = $(this).attr('name')
    });
    $('#SimulatorForm').on('submit', function (event) {
        event.preventDefault();
        if (buttonpressed == "Continuous" && button_counter != 1){
            console.log("Continuous Submission button was pressed.");
            create_post();
            button_counter =1;
            interval_var = setInterval(create_post, 2000);
        }else if (buttonpressed == "Once") {
            console.log("Submit Once button was pressed.");
            if (interval_var) {
                clearInterval(interval_var);
                button_counter =0;
            }
            create_post();
        }else if (buttonpressed == "Stop") {
            console.log("Stopping continuous submission.");
            if (interval_var) {
                clearInterval(interval_var);
                button_counter =0;
            }
        }
    });
    
    // AJAX for posting
    function create_post() {
        console.log("Entered create_post() function.");
        $.ajax({
            url: "", // the endpoint
            type: "POST", // http method
            data: {
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
                current_fuel_level: $('#post-current-fuel-level').val(),
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
        let temperature = parseFloat($('#post-temperature').val());
        let acceleration_x = parseFloat($('#post-acceleration-X').val());
        let acceleration_y = parseFloat($('#post-acceleration-Y').val());
        let acceleration_z = parseFloat($('#post-acceleration-Z').val());
        let wheel_speed_fr = parseFloat($('#post-wheel-speed-fr').val());
        let wheel_speed_fl = parseFloat($('#post-wheel-speed-fl').val());
        let wheel_speed_br = parseFloat($('#post-wheel-speed-br').val());
        let wheel_speed_bl = parseFloat($('#post-wheel-speed-bl').val());
        let suspension_fr = parseFloat($('#post-suspension-fr').val());
        let suspension_fl = parseFloat($('#post-suspension-fl').val());
        let suspension_br = parseFloat($('#post-suspension-br').val());
        let suspension_bl = parseFloat($('#post-suspension-bl').val());
        let current_fuel_level = parseFloat($('#post-current-fuel-level').val());
        if(current_fuel_level <= 10){
            current_fuel_level += 90;
        }
        else{
            current_fuel_level -= getRandomNumber(0,5);
        }
        acceleration_x = acceleration_x + getRandomNumber(-5,5);
        acceleration_y = acceleration_y + getRandomNumber(-5,5);
        acceleration_z = acceleration_z + getRandomNumber(-5,5);
        $('#post-created-at').val(getDateTimenow());
        $('#post-temperature').val(getNextValue(temperature,-5,5));
        $('#post-acceleration-X').val(roundOffAndParse(acceleration_x));
        $('#post-acceleration-Y').val(roundOffAndParse(acceleration_y));
        $('#post-acceleration-Z').val(roundOffAndParse(acceleration_z));
        $('#post-wheel-speed-fr').val(getNextValue(wheel_speed_fr,-5,5));
        $('#post-wheel-speed-fl').val(getNextValue(wheel_speed_fl,-5,5));
        $('#post-wheel-speed-br').val(getNextValue(wheel_speed_br,-5,5));
        $('#post-wheel-speed-bl').val(getNextValue(wheel_speed_bl,-5,5));
        $('#post-suspension-fr').val(getNextValue(suspension_fr,-5,5));
        $('#post-suspension-fl').val(getNextValue(suspension_fl,-5,5));
        $('#post-suspension-br').val(getNextValue(suspension_br,-5,5));
        $('#post-suspension-bl').val(getNextValue(suspension_bl,-5,5));
        $('#post-current-fuel-level').val(roundOffAndParse(current_fuel_level));
    }

    // This function returns current date time in the format "yyyy-mm-dd hh:min:ss"
    function getDateTimenow(){
        var now = new Date();
        var yyyy = now.getFullYear();
        var mm = ("0" + (now.getMonth() + 1)).slice(-2);
        var dd = ("0" + now.getDate()).slice(-2);
        var hours = ("0" + now.getHours()).slice(-2);
        var minutes = ("0" + now.getMinutes()).slice(-2);
        var seconds = ("0" + now.getSeconds()).slice(-2);
        var curr_date = yyyy + '-' + mm + '-' + dd;
        var curr_time = hours + ':' + minutes + ':' + seconds;
        return curr_date + " " + curr_time;
    }

    //This function returns next sensor value, also makes sure that the value is in between 0 and 100
    function getNextValue(sensorValue, min, max){
        let MAX_VALUE = 100;
        let MIN_VALUE = 0;
        if((sensorValue-MIN_VALUE)<Math.abs(min)){
            max = max-min;
            min = 0;
        }
        else if((MAX_VALUE-sensorValue)<Math.abs(max)){
            max = 0;
        }
        nextSensorValue = sensorValue + getRandomNumber(min,max);
        return roundOffAndParse(nextSensorValue);
    }

    //This function returns random number between min(inclusive) and max(exclusive)
    function getRandomNumber(min,max){
        let rand_num = Math.random()*(max-min)+min;
        return rand_num;
    }

    function roundOffAndParse(nextSensorValue){
        rounded = nextSensorValue.toFixed(2);
        return parseFloat(rounded);
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
