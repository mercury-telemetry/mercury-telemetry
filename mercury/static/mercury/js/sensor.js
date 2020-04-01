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

    var newSensorDiv = document.getElementById("add-new-sensor");
    var existingSensorDiv = document.getElementById("existing-sensors");
    var newTypeDiv = document.getElementById("add-new-type");
    var viewTypesDiv = document.getElementById("view-existing-types");
    var editSensorsDiv = document.getElementById("edit-sensors");
    var editSensorTypesDiv = document.getElementById("edit-sensor-types");

    var modifyButton = document.getElementById("current-sensor-btn");
    var newSensorButton = document.getElementById("add-sensor-btn");
    var newTypeButton = document.getElementById("add-sensor-type-btn");
    var viewTypesButton = document.getElementById("view-sensor-types-btn");
    var editSensorsButton = document.getElementById("edit-sensors-btn");
    var editSensorTypesButton = document.getElementById("edit-sensor-types-btn");

    if (sessionStorage.getItem('viewing') == 'addingNew'){
        newSensorDiv.style.display = "block";
        existingSensorDiv.style.display = 'none';
        newTypeDiv.style.display = "none";
        viewTypesDiv.style.display = "none";
        editSensorsDiv.style.display = "none";
        editSensorTypesDiv.style.display = "none";

        modifyButton.style.backgroundColor = 'var(--light-accent)';
        newSensorButton.style.backgroundColor = 'var(--green)';
        newTypeButton.style.backgroundColor = 'var(--light-accent)';
        viewTypesButton.style.backgroundColor = 'var(--light-accent)';
        editSensorsButton.style.backgroundColor = 'var(--light-accent)';
        editSensorTypesButton.style.backgroundColor = 'var(--light-accent)';
    }
    else if (sessionStorage.getItem('viewing') == 'view-sensors'){
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'block';
        newTypeDiv.style.display = "none";
        viewTypesDiv.style.display = "none";
        editSensorsDiv.style.display = "none";
        editSensorTypesDiv.style.display = "none";

        modifyButton.style.backgroundColor = 'var(--green)';
        newSensorButton.style.backgroundColor = 'var(--light-accent)';
        newTypeButton.style.backgroundColor = 'var(--light-accent)';
        viewTypesButton.style.backgroundColor = 'var(--light-accent)';
        editSensorsButton.style.backgroundColor = 'var(--light-accent)';
        editSensorTypesButton.style.backgroundColor = 'var(--light-accent)';
    }
    else if (sessionStorage.getItem('viewing') == 'addingNewType'){
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'none';
        newTypeDiv.style.display = "block";
        viewTypesDiv.style.display = "none";
        editSensorsDiv.style.display = "none";
        editSensorTypesDiv.style.display = "none";

        modifyButton.style.backgroundColor = 'var(--light-accent)';
        newSensorButton.style.backgroundColor = 'var(--light-accent)';
        newTypeButton.style.backgroundColor = 'var(--green)';
        viewTypesButton.style.backgroundColor = 'var(--light-accent)';
        editSensorsButton.style.backgroundColor = 'var(--light-accent)';
        editSensorTypesButton.style.backgroundColor = 'var(--light-accent)';
    }
    else if (sessionStorage.getItem('viewing') == 'viewingTypes'){
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'none';
        newTypeDiv.style.display = "none";
        viewTypesDiv.style.display = "block";
        editSensorsDiv.style.display = "none";
        editSensorTypesDiv.style.display = "none";

        modifyButton.style.backgroundColor = 'var(--light-accent)';
        newSensorButton.style.backgroundColor = 'var(--light-accent)';
        newTypeButton.style.backgroundColor = 'var(--light-accent)';
        viewTypesButton.style.backgroundColor = 'var(--green)';
        editSensorsButton.style.backgroundColor = 'var(--light-accent)';
        editSensorTypesButton.style.backgroundColor = 'var(--light-accent)';
    }
    else if (sessionStorage.getItem('viewing') == 'editingSensors'){
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'none';
        newTypeDiv.style.display = "none";
        viewTypesDiv.style.display = "none";
        editSensorsDiv.style.display = "block";
        editSensorTypesDiv.style.display = "none";

        modifyButton.style.backgroundColor = 'var(--light-accent)';
        newSensorButton.style.backgroundColor = 'var(--light-accent)';
        newTypeButton.style.backgroundColor = 'var(--light-accent)';
        viewTypesButton.style.backgroundColor = 'var(--light-accent)';
        editSensorsButton.style.backgroundColor = 'var(--green)';
        editSensorTypesButton.style.backgroundColor = 'var(--light-accent)';
    }
    else if (sessionStorage.getItem('viewing') == 'editingSensorTypes'){
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'none';
        newTypeDiv.style.display = "none";
        viewTypesDiv.style.display = "none";
        editSensorsDiv.style.display = "none";
        editSensorTypesDiv.style.display = "block";

        modifyButton.style.backgroundColor = 'var(--light-accent)';
        newSensorButton.style.backgroundColor = 'var(--light-accent)';
        newTypeButton.style.backgroundColor = 'var(--light-accent)';
        viewTypesButton.style.backgroundColor = 'var(--light-accent)';
        editSensorsButton.style.backgroundColor = 'var(--light-accent)';
        editSensorTypesButton.style.backgroundColor = 'var(--green)';
    }
    else {
        displayCurrentSensors()
    }
}

function displayCurrentSensors() {
    sessionStorage.setItem('viewing', 'view-sensors');
    selectView()
}

function displayAddNewSensor() {
  sessionStorage.setItem('viewing', 'addingNew');
  selectView()
}

function displayAddNewSensorType() {
    sessionStorage.setItem('viewing', 'addingNewType');
    selectView()
}

function displaySensorTypes() {
    sessionStorage.setItem('viewing', 'viewingTypes');
    selectView()
}

function displayEditSensors() {
    sessionStorage.setItem('viewing', 'editingSensors');
    selectView()
}

function displayEditSensorTypes() {
    sessionStorage.setItem('viewing', 'editingSensorTypes');
    selectView()
}
