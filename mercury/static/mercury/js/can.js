$(function () {

    // Submit post on submit
    $('#CanForm').on('submit', function (event) {
        event.preventDefault();
        console.log("Submit CAN Message button was pressed.");
        create_post();
        }
    );

    // AJAX for posting
    function create_post() {
        console.log("Entered create_post() function.");
        $.ajax({
            url: "/api/can/", // the endpoint
            type: "POST", // http method
            data: {
                can_msg: $('#id_can_msg').val()
            }, // data sent with the post request

            // handle a successful response
            success: function (response) {
                console.log("POSTing was successful.");
                console.log("Response:" + response);
                let json_resp = JSON.stringify(response, null, 4).replace(/\\/g, "").replace(/,/g, ",\n");
                document.getElementById("can-result").innerHTML = json_resp;
            },

            // handle a non-successful response
            error: function (xhr, errmsg) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                let json_resp = JSON.stringify(xhr.responseText, null, 4).replace(/\\/g, "").replace(/,/g, ",\n");
                document.getElementById("can-result").innerHTML = json_resp;

            }
        });
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
