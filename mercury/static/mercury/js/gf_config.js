function toggleButton(button_name){
    resetButtons();
    resetRadio();

    if (button_name == "existing-gf-hosts"){
        $('#existing-gf-hosts').removeClass("hide-display");
    } else if (button_name == "add-gf-host"){
        $('#add-gf-host').removeClass("hide-display");
    } else if (button_name == "update-gf-config"){
        $('#update-gf-config').removeClass("hide-display");
    } else if (button_name == "help-gf-config"){
        $('#help-gf-config').removeClass("hide-display");
    }
}

function radioSelect(selection){
    var usernames = document.querySelectorAll("#div_id_gf_username");
    var passwords = document.querySelectorAll("#div_id_gf_password");
    var tokens = document.querySelectorAll("#div_id_gf_token");
    if (selection == "api"){
        for (var i = 0; i < usernames.length; i++) {
            usernames[i].classList.add("hide-display");
        }
        for (var i = 0; i < passwords.length; i++) {
            passwords[i].classList.add("hide-display");
        }
        for (var i = 0; i < tokens.length; i++) {
            tokens[i].classList.remove("hide-display");
        }
    } else if (selection == "login") {
        for (var i = 0; i < usernames.length; i++) {
            usernames[i].classList.remove("hide-display");
        }
        for (var i = 0; i < passwords.length; i++) {
            passwords[i].classList.remove("hide-display");
        }
        for (var i = 0; i < tokens.length; i++) {
            tokens[i].classList.add("hide-display");
        }
    }
}


function resetRadio() {
    var usernames = document.querySelectorAll("#div_id_gf_username");
    var passwords = document.querySelectorAll("#div_id_gf_password");
    var tokens = document.querySelectorAll("#div_id_gf_token");
    for (var i = 0; i < usernames.length; i++) {
        usernames[i].classList.remove("hide-display");
    }
    for (var i = 0; i < passwords.length; i++) {
        passwords[i].classList.remove("hide-display");
    }
    for (var i = 0; i < tokens.length; i++) {
        tokens[i].classList.add("hide-display");
    }
    if (document.getElementById("radioLogin") !== null) {
        document.getElementById("radioLogin").checked = true;
    }
    if (document.getElementById("radioLogin2") !== null) {
        document.getElementById("radioLogin2").checked = true;
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
    resetRadio();
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
    $('#update-gf-config').addClass('hide-display');
}
