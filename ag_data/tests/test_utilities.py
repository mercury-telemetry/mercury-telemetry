from django.test import TestCase

from ag_data.models import AGSensorType
from ag_data.presets import built_in_sensor_types as bist

from ag_data import utilities


class UtilityFunctionsTest(TestCase):
    def test_createOrResetBuiltInSensorTypeAtPresetIndex(self):
        totalTestSensorTypes = len(bist.built_in_sensor_types)

        # test sensor type creation for indices in range

        for index in range(totalTestSensorTypes):

            # test object (sensor type) creation

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            expected_sensor_type = bist.built_in_sensor_types[index]

            sensorType = AGSensorType.objects.get(
                pk=expected_sensor_type["agSensorTypeID"]
            )

            self.assertEqual(sensorType.name, expected_sensor_type["agSensorTypeName"])
            self.assertEqual(
                sensorType.processing_formula,
                expected_sensor_type["agSensorTypeFormula"],
            )
            self.assertEqual(
                sensorType.format, expected_sensor_type["agSensorTypeFormat"]
            )

            # test object (sensor type) reset

            sensorType.name = expected_sensor_type["agSensorTypeName"] + " "
            sensorType.processing_formula = (
                expected_sensor_type["agSensorTypeFormula"] + 1
            )
            sensorType.format = [expected_sensor_type["agSensorTypeFormat"]]
            sensorType.save()

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            sensorType = AGSensorType.objects.get(
                pk=expected_sensor_type["agSensorTypeID"]
            )

            self.assertEqual(sensorType.name, expected_sensor_type["agSensorTypeName"])
            self.assertEqual(
                sensorType.processing_formula,
                expected_sensor_type["agSensorTypeFormula"],
            )
            self.assertEqual(
                sensorType.format, expected_sensor_type["agSensorTypeFormat"]
            )

        # test sensor type creation for index out of range

        with self.assertRaises(Exception) as e:
            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(totalTestSensorTypes)

        correct_exception_message = (
            "Cannot find requested sensor type (index "
            + str(totalTestSensorTypes)
            + ") from presets"
        )

        self.assertEqual(str(e.exception), correct_exception_message)
