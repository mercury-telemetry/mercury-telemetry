from django.test import TestCase

from ag_data.models import AGSensorType
from ag_data.presets import built_in_sensor_types as bist

from ag_data import utilities


class UtilityFunctionUnitTest(TestCase):
    def setUp(self):
        self.totalTestSensorTypes = len(bist.built_in_sensor_types)

    def test_createOrResetBuiltInSensorTypeAtPresetIndex_creation(self):

        for index in range(self.totalTestSensorTypes):

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            reference = bist.built_in_sensor_types[index]

            self.checkSensorTypeRecord(reference)

    def test_createOrResetBuiltInSensorTypeAtPresetIndex_reset(self):

        for index in range(self.totalTestSensorTypes):

            reference = bist.built_in_sensor_types[index]

            utilities.createOrResetBuiltInSensorTypeAtPresetIndex(index)

            sensorType = AGSensorType.objects.get(pk=reference["agSensorTypeID"])

            sensorType.name = reference["agSensorTypeName"] + " "
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
            "Cannot find requested sensor type (index "
            + str(self.totalTestSensorTypes)
            + ") from presets"
        )

        self.assertEqual(str(e.exception), correct_exception_message)

    def checkSensorTypeRecord(self, reference):
        sensorType = AGSensorType.objects.get(pk=reference["agSensorTypeID"])

        self.assertEqual(sensorType.name, reference["agSensorTypeName"])
        self.assertEqual(
            sensorType.processing_formula, reference["agSensorTypeFormula"]
        )
        self.assertEqual(sensorType.format, reference["agSensorTypeFormat"])
