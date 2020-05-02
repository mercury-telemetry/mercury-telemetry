# Configure Sensors
To navigate to the configure sensors page, click on the "Configure Sensors" icon on the left side of the webpage. The configure sensors page is broken into two components: adding new sensors and managing existing sensors. 

## Adding New Sensors
In order to add a sensor to your Mercury instance, you must use the following Add Sensor Form.
![Add Sensor Form](imgs/add_sensor_form.png)


- Sensor Name
  - To add a new sensor, first type a name into the sensor name box. 
  - Restrictions:
    - All sensors must have non-empty names.
    - You cannot have two sensors with the same name in the database. Note that all sensor names are stored in lowercase in the database, so this restriction is NOT case sensitive.
- Fields
  - Once you decided on the sensor name, it's time to give your sensor some fields. For some sensors, such as a temperature sensor, one field is enough. In this case, it is perfectly acceptable to name your field the same as your sensor name.
  - For other sensors, such as a triple-axis accelerometer, multiple fields are required. In this case, you can click the green "+" button beneath the "Unit" box to add a new field. Notice that each field row also has an "X" to the right of its unit box; if you accidentally inserted too many fields, you can always delete any of the fields with this "X" button. However, there always must be at least one field per sensor. This is enforced by our UI, so don't worry about deleting too many fields; the app won't let you.
  - For each field, there are three potential data types: numeric (float), character (string), and boolean. Choose whatever data type is appropriate for each individual field.
  - Each field has a "Unit" option for user convenience. Units are not mandated for each field.
  - Restrictions
    - One sensor cannot have two fields with the same name.
    - All fields must have non-empty names.
- Graph Type
  - On the bottom of the add sensor form you will see a dropdown labeled Graph Type. Here you can choose the default way that data from the sensor will be viewed on Grafana. 
  - Further graph customization options (bar graphs, absolute values, etc) are available within your Grafana instance.
- Once you've added all of your sensor fields and chosen the default graph type for Grafana, hit the "Add New Sensor" button at the bottom of the form. The sensor will then be saved in the database and a panel with the graph type you chose will be created automatically in Grafana.

### Adding GPS Sensor
The GPS sensor receives special treatment in Mercury. In order to add a GPS Sensor, you must give exactly two fields with the names "latitude" and "longitude". You also must choose "Map" as your graph type. The sensor name can be whatever you wish, so long as it complies with the restrictions listed above. An example of a properly-formatted GPS sensor can be seen below:
![Add Sensor Form](imgs/add_sensor_gps.png)


## Viewing Existing Sensors