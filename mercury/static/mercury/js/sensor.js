function addRow(){
  var sensorList, field_name_li, field_type_li, field_name_input, field_type_select,
  float_option, string_option, bool_option;

  sensorList = document.getElementById("sensor-list");
  // Make name box:
  field_name_li = document.createElement("li");
  field_name_li.className = "sensor-list-field-name";
  field_name_input = document.createElement("input");
  field_name_input.setAttribute("type","text");
  field_name_input.setAttribute("name","field-name")
  field_name_li.appendChild(field_name_input);
  sensorList.appendChild(field_name_li);

  //Make field type:
  field_type_li = document.createElement("li");
  field_type_li.className = "sensor-list-field-type";
  field_type_select = document.createElement("select");
  field_type_select.setAttribute("name", "field-type")

  float_option = document.createElement("option");
  float_option.appendChild(document.createTextNode("Float"));
  field_type_select.appendChild(float_option);

  string_option = document.createElement("option");
  string_option.appendChild(document.createTextNode("String"));
  field_type_select.appendChild(string_option);

  bool_option = document.createElement("option");
  bool_option.appendChild(document.createTextNode("Boolean"));
  field_type_select.appendChild(bool_option);

  field_type_li.appendChild(field_type_select);
  sensorList.appendChild(field_type_li);

  var hr = document.createElement('hr');
  sensorList.appendChild(hr);
}

var add_field_button = document.getElementById("addfieldbutton");
add_field_button.onclick = function() {
  addRow();
}
