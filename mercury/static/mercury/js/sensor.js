$(document).ready(function () {

  // create an event handler for each sensor form
  $('form[name="sensor_edit_form"]').submit(function(event) {
    event.preventDefault();

    var sensor_id = event.target.elements["sensor-id"].value;
    var sensor_name = event.target.elements["sensor-name"].value;

    // sensor_data_exists takes a sensor id as a parameter and returns a JSON object
    // with the element "status", which is True if data exists for this sensor,
    // and False otherwise.
    $.ajax({
        url: `/sensor_data_exists/${sensor_id}`,
        type: "GET",

        success: function(response) {

            var data = JSON.parse(response);

            if (data["status"] == true) {
                runUpdateWarning(event, sensor_name);

            } else {
                event.target.submit();
            }
        },

        // run the update warning even if ajax fails (prevent user from missing the warning)
        error: function() {
            runUpdateWarning(event, sensor_name);
        }
    });
  });
});

function runUpdateWarning(event, sensor_name){
    var warning_id = `${sensor_name}-update-warning`;
    warning = document.getElementById(warning_id);

    console.log('hide modify/update/delete buttons');
    // hide update button
    var update_button_id = `${sensor_name}-submit-button`;
    var delete_button_id = `${sensor_name}-delete-button`;
    var cancel_button_id = `${sensor_name}-cancel-button`;
    console.log(update_button_id);
    update_button = document.getElementById(update_button_id);
    delete_button = document.getElementById(delete_button_id);
    cancel_button = document.getElementById(cancel_button_id);

    update_button.style.display = "none";
    delete_button.style.display = "none";
    cancel_button.style.display = "none";

    // show update warning
    warning.style.display = "block";

    // attach event handlers to update warning buttons
    $("#update-continue").click(function(){
        // submit the form
        event.target.submit();
    });
    $("#update-cancel").click(function(){
        // hide warning
        warning.style.display = "none";
        update_button.style.display = "block";
        delete_button.style.display = "block";
        cancel_button.style.display = "block";


        // show update button
        update_button = "block";
    });
    $("#update-export").click(function(){
        // redirect
        window.location.replace(Urls["mercury:events"]());
    });
}

function addRow(table_name){
    var table = document.getElementById(table_name);
    var rowCount = table.rows.length;
    var colCount = table.rows[0].cells.length;
    var newRow = table.insertRow(rowCount-1);
    newRow.className = "sensor-fields-table-tr"
    for(var i=0; i<colCount; i++){
        var newCell = newRow.insertCell(i);
        /* set new cell to be same as cell in first data (non-header) row */
        newCell.innerHTML = table.rows[1].cells[i].innerHTML
        newCell.className = "sensor-fields-table-td"
    }
}

function deleteRow(table_name, row) {
    var table = document.getElementById(table_name);
    if (table.rows.length > 3) {
        table.deleteRow(row);
    }
}

function makeSensorEditable(sensor_name, offset) {
    var displayViews = ["none", "block"];
    var view_name = sensor_name.concat("-view");
    var edit_name = sensor_name.concat("-edit");
    var view_sensors = document.getElementsByClassName(view_name);
    var edit_sensors = document.getElementsByClassName(edit_name);
    for(item of view_sensors){
        item.style.display = displayViews[offset];
    }
    for(item of edit_sensors){
        item.style.display = displayViews[1-offset];
    }
    var edit_button_name = sensor_name.concat("-edit-button")
    document.getElementById(edit_button_name).style.display = displayViews[offset];

    var submit_button_name = sensor_name.concat("-submit-button")
    document.getElementById(submit_button_name).style.display = displayViews[1-offset];

    var cancel_button_name = sensor_name.concat("-cancel-button")
    document.getElementById(cancel_button_name).style.display = displayViews[1-offset];

    var delete_button_name = sensor_name.concat("-delete-button")
    document.getElementById(delete_button_name).style.display = displayViews[1-offset];
}
