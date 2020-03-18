function addRow(){
    var table = document.getElementById("new-sensor-table");
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
    var table = document.getElementById("new-sensor-table");
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
    var modifyButton = document.getElementById("current-sensor-btn");
    var newButton = document.getElementById("add-sensor-btn");
    if (sessionStorage.getItem('viewing') == 'addingNew'){
        newSensorDiv.style.display = "block";
        existingSensorDiv.style.display = 'none';

        modifyButton.style.backgroundColor = 'var(--light-accent)';
        newButton.style.backgroundColor = 'var(--green)';
    }
    else {
        newSensorDiv.style.display = "none";
        existingSensorDiv.style.display = 'block';

        modifyButton.style.backgroundColor = 'var(--green)';
        newButton.style.backgroundColor = 'var(--light-accent)';
    }
}

function displayCurrentSensors() {
    sessionStorage.setItem('viewing', 'existing');
    selectView()
}

function displayAddNewSensor() {
  sessionStorage.setItem('viewing', 'addingNew');
  selectView()
}
