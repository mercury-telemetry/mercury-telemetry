function addRow(){
    var table = document.getElementById("new-type-table");
    var rowCount = table.rows.length;
    var colCount = table.rows[0].cells.length;
    var newRow = table.insertRow(rowCount);
    for(var i=0; i<colCount; i++){
        var newCell = newRow.insertCell(i);
        /* set new cell to be same as cell in first data (non-header) row */
        newCell.innerHTML = table.rows[1].cells[i].innerHTML
    }
    table.rows[rowCount].cells[0].innerHTML =rowCount
}

function deleteRow() {
    var table = document.getElementById("new-type-table");
    var rowCount = table.rows.length;
    if (rowCount > 2){
        table.deleteRow(rowCount-1)
    }
}

/*
selectView displays the correct view of the "Add or Modify Sensors" page
-the default view is to show existing sensors
-if a user submits a new sensor which posts and reloads page, then the add new sensor view should remain
*/
function selectView() {
    var existingSensorDiv = document.getElementById("existing-sensors");
    var newSensorDiv = document.getElementById("add-new-sensor");
    var viewSensorsButton = document.getElementById("current-sensor-btn");
    var newSensorButton = document.getElementById("add-sensor-btn");

    if (sessionStorage.getItem('viewing') == 'addingNew'){
        newSensorDiv.style.display = "block";
        existingSensorDiv.style.display = 'none';
        viewSensorsButton.style.backgroundColor = 'var(--light-accent)';
        newSensorButton.style.backgroundColor = 'var(--green)';
    }
    else if (sessionStorage.getItem('viewing') == 'existing'){
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'block';
        viewSensorsButton.style.backgroundColor = 'var(--green)';
        newSensorButton.style.backgroundColor = 'var(--light-accent)';
    }
    /*Added to prevent undesired behavior when opening sensors in new browser tab*/
    else {displayCurrentSensors()}
}

function displayCurrentSensors() {
    sessionStorage.setItem('viewing', 'existing');
    selectView()
}

function displayAddNewSensor() {
  sessionStorage.setItem('viewing', 'addingNew');
  selectView()
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
