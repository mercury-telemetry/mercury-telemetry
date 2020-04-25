$(document).ready(function () {

  $('[name="sensor-graph-type"').change(function(event) {

        select = event.target;
        id = event.target.id;
        if (id.indexOf("_") == -1) {
            sensor_id = "";
        } else {
            sensor_id = event.target.id.substring(id.indexOf("_") + 1);
        }

        var currentOption = select.options[select.selectedIndex].value;

        if (sensor_id !== "") {
            var graphImg = $(`div#graph${sensor_id}`)[0];
            var mapImg = $(`div#map${sensor_id}`)[0];
            var gaugeImg = $(`div#gauge${sensor_id}`)[0];
        } else {
            var graphImg = $("div#graph")[0];
            var mapImg = $("div#map")[0];
            var gaugeImg = $("div#gauge")[0];
        }

        if (currentOption == "graph"){
            graphImg.style.display = "block";
            mapImg.style.display = "none";
            gaugeImg.style.display = "none";
        }
        else if (currentOption == "map") {
            mapImg.style.display = "block";
            graphImg.style.display = "none";
            gaugeImg.style.display = "none";
        }
        else if (currentOption == "gauge") {
            gaugeImg.style.display = "block";
            graphImg.style.display = "none";
            mapImg.style.display = "none";

        }
    });

  // create an event handler for each update sensor form
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
        dataType: "json",

        success: function(response) {

            var data = response;

            if (data["status"] == true) {
                runWarning(event, sensor_name, sensor_id, "update");

            } else {
                event.target.submit();
            }
        },

        // run the update warning even if ajax fails (prevent user from missing the warning)
        error: function() {
            runWarning(event, sensor_name, sensor_id, "update");
        }
    });
  });

  // create an event handler for each delete sensor form
    $('form[name="delete-sensor-form"]').submit(function(event) {

        event.preventDefault();

        var sensor_id = event.target.elements["sensor-id"].value;
        var sensor_name = event.target.elements["sensor-name"].value;

        $.ajax({
            url: `/sensor_data_exists/${sensor_id}`,
            type: "GET",
            dataType: "json",

            success: function(response) {

                var data = response;

                if (data["status"] == true) {
                    runWarning(event, sensor_name, sensor_id, "delete");

                } else {
                    event.target.submit();
                }
            },

            // run the update warning even if ajax fails (prevent user from missing the warning)
            error: function() {
                runWarning(event, sensor_name, sensor_id, "delete");
            }
        });

    });
});



// warning_type is either 'update' or 'delete'
function runWarning(event, sensor_name, sensor_id, warning_type){
    var warning_id = `${sensor_id}-${warning_type}-warning`;
    warning = document.getElementById(warning_id);

    // hide update/delete/cancel buttons
    var update_button_id = `${sensor_name}-submit-button`;
    var delete_button_id = `${sensor_name}-delete-button`;
    var cancel_button_id = `${sensor_name}-cancel-button`;

    update_button = document.getElementById(update_button_id);
    delete_button = document.getElementById(delete_button_id);
    cancel_button = document.getElementById(cancel_button_id);

    update_button.style.display = "none";
    delete_button.style.display = "none";
    cancel_button.style.display = "none";

    // show update warning
    warning.style.display = "block";

    // attach event handlers to update warning buttons

    $(`#${sensor_id}-${warning_type}-continue`).click(function(){
        // submit the form
        event.target.submit();
    });

    var warningCancel = $(`#${sensor_id}-${warning_type}-cancel`);
    warningCancel.click(function(){
        // hide warning
        warning.style.display = "none";
        update_button.style.display = "block";
        delete_button.style.display = "block";
        cancel_button.style.display = "block";

        // show update button
        update_button = "block";
    });
    $(`#${sensor_id}-${warning_type}-export`).click(function(){
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
