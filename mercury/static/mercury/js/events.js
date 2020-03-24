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
    }
}

function resetEventButtons(){
    $('#all-events').addClass('hide-display')
    $('#all-venues').addClass('hide-display')
    $('#create-event').addClass('hide-display')
    $('#update-event').addClass('hide-display')
    $('#update-venue').addClass('hide-display')
    $('#create-venue').addClass('hide-display')
}
