$(document).ready(function() {

    // create an event handler for each delete sensor form
    $('[name="delete-event"]').click(function(event, preventDefault=true) {

        if (preventDefault) {
            event.preventDefault();
        }

        var event_id = event.target.id;

        $.ajax({
            url: `/event_data_exists/${event_id}`,
            type: "GET",
            dataType: "json",

            success: function(response) {

                var data = response;

                if (data["status"] == true) {
                    runWarning(event_id, event.target);

                } else {
                    $(`form#${event_id}-delete-form`).submit();
                }
            },

            // run the update warning even if ajax fails (prevent user from missing the warning)
            error: function() {
                runWarning(event_id, event.target);
            }
        });

    });

})

// run warning - measurements will be deleted before
// deleting the event
function runWarning(event_id, delete_button){
    var warning_id = `${event_id}-warning`;
    warning = document.getElementById(warning_id);

    // hide delete button

    //var delete_button_id = '[name="delete-event"]';
    //delete_button = document.getElementById(delete_button_id);
    delete_button.style.display = "none";

    // show update warning
    warning.style.display = "block";

    // attach event handlers to update warning buttons
    $(`button#${event_id}-warning-continue`).click(function(){
        $(`form#${event_id}-delete-form`).submit();
    });

    var cancel_id = `${event_id}-warning-cancel`;
    var warningCancel = document.getElementById(cancel_id);
    warningCancel.click(function(){
        // hide warning
        warning.style.display = "none";

        // show delete button
        delete_button.style.display = "block";
    });
    $(`#${event_id}-warning-export`).click(function(){
        // redirect
        window.location.replace(Urls["mercury:events"]());
    });
}

function toggleEventButton(button_name){
    resetEventButtons();
    
    if (button_name == "all_events"){
        $('#all-events').removeClass("hide-display");
    } else if (button_name == "create_event"){
        $('#create-event').removeClass("hide-display");
    } else if (button_name == "update_event"){
        $('#update-event').removeClass("hide-display");
    } else if (button_name == "all_venues"){
        $('#all-venues').removeClass("hide-display");
    } else if (button_name == "create_venue"){
        $('#create-venue').removeClass("hide-display");
    } else if (button_name == "update_venue"){
        $('#update-venue').removeClass("hide-display");
    } else if (button_name == "help-events"){
        $('#help-events').removeClass("hide-display");
    }
}

function resetEventButtons(){
    $('#all-events').addClass('hide-display')
    $('#all-venues').addClass('hide-display')
    $('#create-event').addClass('hide-display')
    $('#update-event').addClass('hide-display')
    $('#update-venue').addClass('hide-display')
    $('#create-venue').addClass('hide-display')
    $('#help-events').addClass('hide-display')
}
