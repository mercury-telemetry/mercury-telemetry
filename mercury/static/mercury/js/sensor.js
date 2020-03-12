function addRow(){
  var sensorList, field_name_li, field_type_li, field_name_input, field_type_select,
  float_option, string_option, bool_option;

  fields = document.getElementById("field-list");
  // Make field name input
  field_name_input = document.createElement("input");
  field_name_input.setAttribute("type","text");
  field_name_input.setAttribute("name","field-name");
  field_name_input.setAttribute("class","inline-block-child");
  fields.appendChild(field_name_input);

  //Make field type
  field_type_select = document.createElement("select");
  field_type_select.setAttribute("name", "field-type");
  field_type_select.setAttribute("class", "inline-block-child");

  float_option = document.createElement("option");
  float_option.setAttribute("value", "float");
  float_option.appendChild(document.createTextNode("Float"));
  field_type_select.appendChild(float_option);

  string_option = document.createElement("option");
  string_option.setAttribute("value", "string");
  string_option.appendChild(document.createTextNode("String"));
  field_type_select.appendChild(string_option);

  bool_option = document.createElement("option");
  bool_option.setAttribute("value", "bool");
  bool_option.appendChild(document.createTextNode("Boolean"));
  field_type_select.appendChild(bool_option);

  fields.appendChild(field_type_select);

  // Make unit input
  unit_input = document.createElement("input");
  unit_input.setAttribute("type","text");
  unit_input.setAttribute("name","field-unit")
  unit_input.setAttribute("class", "inline-block-child");
  fields.appendChild(unit_input);

  var hr = document.createElement('hr');
  fields.appendChild(hr);
}

var add_field_button = document.getElementById("addfieldbutton");
add_field_button.onclick = function() {
  addRow();
}
