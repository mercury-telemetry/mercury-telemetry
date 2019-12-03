$(function () {

    // Submit post on submit
    $('#CanForm').on('submit', function (event) {
        event.preventDefault();
        console.log("Submit CAN Message button was pressed.");
        create_post();
        }
    );
    function creating_table(list) {
            var cols = [];
            for (var i = 0; i < list.length; i++) {
                for (var k in list[i]) {
                    if (cols.indexOf(k) === -1) {

                        // Push all keys to the array
                        cols.push(k);
                    }
                }
            }
            // Create a table element
            var table = document.createElement("table");
            for (var i = 0; i < cols.length; i++) {

                // Create the table header th element
                var tr = table.insertRow(-1);
                var theader = document.createElement("th");
                theader.innerHTML = cols[i];
                // Append columnName to the table row
                tr.appendChild(theader);
                var cell = tr.insertCell(-1);
                cell.innerHTML = list[0][cols[i]];
            }


            // Add the newely created table containing json data
            var el = document.getElementById("table");
            el.innerHTML = "";
            el.appendChild(table);
        }
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

                creating_table([response["can_msg"]]);
                document.getElementById("para").innerHTML = "";
                document.getElementById("para2").innerHTML = "";
            },

            // handle a non-successful response
            error: function (xhr, errmsg) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console


                var obj = JSON.parse(xhr.responseText);
                document.getElementById("para").innerHTML = "Error: "+obj.error;
                document.getElementById("para2").innerHTML = "Received Message: "+obj.received_message;

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
