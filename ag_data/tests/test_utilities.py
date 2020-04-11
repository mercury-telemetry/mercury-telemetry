from django.test import TestCase

from ag_data.models import AGSensorType
from ag_data.presets import built_in_content as built_in_content

from ag_data import utilities


class UtilityFunctionUnitTest(TestCase):
    def setUp(self):
        self.totalTestSensorTypes = len(built_in_content.built_in_sensor_types)

    def test_createOrResetAllBuiltInSensorTypes(self):

        utilities.createOrResetAllBuiltInSensorTypes()

        self.assertEqual(AGSensorType.objects.count(), self.totalTestSensorTypes)

        for index in range(self.totalTestSensorTypes):
            reference = built_in_content.built_in_sensor_types[index]

            self.checkSensorTypeRecord(reference)

    def test_createOrResetBuiltInSensorTypeAtPresetIndex_creation(self):

        for index in range(self.totalTestSensorTypes):
            reference = built_in_content.built_in_sensor_types[index]

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            self.checkSensorTypeRecord(reference)

    def test_createOrResetBuiltInSensorTypeAtPresetIndex_reset(self):

        for index in range(self.totalTestSensorTypes):
            reference = built_in_content.built_in_sensor_types[index]

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            sensorType = AGSensorType.objects.get(pk=reference["agSensorTypeID"])

            sensorType.name = reference["agSensorTypeName"].join(" ")
            sensorType.processing_formula = reference["agSensorTypeFormula"] + 1
            sensorType.format = [reference["agSensorTypeFormat"]]
            sensorType.save()

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            self.checkSensorTypeRecord(reference)

    def test_createOrResetBuiltInSensorTypeAtPresetIndex_index_out_of_range(self):

        with self.assertRaises(Exception) as e:
            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(
                self.totalTestSensorTypes
            )

        correct_exception_message = (
            f"Cannot find requested sensor type "
            f"(index {self.totalTestSensorTypes}) from presets"
        )

        self.assertEqual(str(e.exception), correct_exception_message)

    def test_createCustomSensorType(self):
        name = "Custom Sensor Type Name"
        processing_formula = 9
        custom_format = {
            "reading": {"field1": {"unit": "unitA", "format": "float"}},
            "result": {"field2": {"unit": "unitB", "format": "bool"}},
        }

        # called when table empty
        newRecord = utilities.createCustomSensorType(
            name, processing_formula, custom_format
        )

        self.assertTrue(newRecord.id % 2 == 1)
        self.assertEqual(AGSensorType.objects.count(), 1)

        # called when table not empty
        newRecord = utilities.createCustomSensorType(
            name, processing_formula, custom_format
        )

        self.assertTrue(newRecord.id % 2 == 1)
        self.assertEqual(AGSensorType.objects.count(), 2)

        # called when table with one built-in record
        utilities.createOrResetBuiltInSensorTypeAtPresetIndex(0)
        newRecord = utilities.createCustomSensorType(
            name, processing_formula, custom_format
        )

        self.assertTrue(newRecord.id % 2 == 1)
        self.assertEqual(AGSensorType.objects.count(), 4)

        # called when table with multiple built-in records
        utilities.createOrResetAllBuiltInSensorTypes()
        newRecord = utilities.createCustomSensorType(
            name, processing_formula, custom_format
        )

        self.assertTrue(newRecord.id % 2 == 1)
        self.assertEqual(AGSensorType.objects.count(), self.totalTestSensorTypes + 4)

    def checkSensorTypeRecord(self, reference):
        sensorType = AGSensorType.objects.get(pk=reference["agSensorTypeID"])

        self.assertEqual(sensorType.name, reference["agSensorTypeName"])
        self.assertEqual(
            sensorType.processing_formula, reference["agSensorTypeFormula"]
        )
        self.assertEqual(sensorType.format, reference["agSensorTypeFormat"])
