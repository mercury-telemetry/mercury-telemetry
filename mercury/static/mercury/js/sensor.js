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
