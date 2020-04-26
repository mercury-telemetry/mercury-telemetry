function toggleButton(button_name){
    resetButtons();

    if (button_name == "existing-gf-hosts"){
        $('#existing-gf-hosts').removeClass("hide-display");
    } else if (button_name == "add-gf-host"){
        $('#add-gf-host').removeClass("hide-display");
    } else if (button_name == "help-gf-config"){
        $('#help-gf-config').removeClass("hide-display");
    }
}

$(document).ready(function(){

    $('button[name="show-dashboards"]').click(function(event){

       // find all other iframes and hide them
       $('iframe[name="show-dashboards-iframe"]').addClass("hide-display");

       // only display this div
       console.log(`iframe#dashboard_${event.target.id}`);
       $(`iframe#dashboard_${event.target.id}`).removeClass("hide-display");

    });
});


function toggleDashboardButton(button_name){
    resetButtons();

    console.log(button_name);
    console.log(type(button_name));

    if (button_name == "#existing-gf-hosts"){
        $('#existing-gf-hosts').removeClass("hide-display");
    } else if (button_name == "add-gf-host"){
        $('#add-gf-host').removeClass("hide-display");
    } else if (button_name == "help-gf-config"){
        $('#help-gf-config').removeClass("hide-display");
    }

}


function resetButtons(){
    $('[name="show-dashboards-iframe"]').addClass("hide-display");
    $('#existing-gf-hosts').addClass('hide-display');
    $('#add-gf-host').addClass('hide-display');
    $('#help-gf-config').addClass('hide-display');
}
