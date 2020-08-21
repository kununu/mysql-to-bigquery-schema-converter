import unittest
import converter
import json
import os
from utils.bigquery_types_config import BIGQUERY_TYPES

TEST_DATA_PATH = "test_data/"
TYPES_MAP_PATH = TEST_DATA_PATH + "type_mappings_map.json"
FIELD_MAP_PATH = TEST_DATA_PATH + "field_mappings_map.json"
INVALID_TYPES_MAP_PATH = TEST_DATA_PATH + "invalid_type_mappings_map.json"
INVALID_FIELDS_MAP_PATH = TEST_DATA_PATH + "invalid_field_mappings_map.json"


class TestConverter(unittest.TestCase):
    maxDiff = None

    def test_output_correctly_generated_default(self):
        """
        Test if converted mysql schema matches with the BigQuery json one.
        Loop through two input folders. `.sql` and `.json` files must have
        the same name in order to be compared.
        """

        for entry in os.scandir(TEST_DATA_PATH):
            if entry.name.endswith(".sql") and entry.name.startswith('default_'):
                table_name = entry.name.split(".")[0]

                # Find the corresponding .json file for the .sql input
                big_query_json = TEST_DATA_PATH + table_name + ".json"
                with open(big_query_json) as json_file:
                    bigquery_data = json.load(json_file)

                _, big_query_list = converter.convert(entry.path, None, None)
                self.assertEqual(bigquery_data, big_query_list,
                                 msg=f"\nFAILED AT FOLLOWING SCHEMA: {table_name}")

    def test_output_type_mappings_case(self):
        """
        Test if the converted schema is correct when providing a custom data type mapping.
        The custom map is provided via CLI with the '-t', '--extra-type-mappings' option.
        """
        for entry in os.scandir(TEST_DATA_PATH):
            if entry.name.endswith(".sql") and entry.name.startswith('type_mappings_'):
                table_name = entry.name.split(".")[0]

                # Find the corresponding .json file for the .sql input
                big_query_json = TEST_DATA_PATH + table_name + ".json"
                with open(big_query_json) as json_file:
                    bigquery_data = json.load(json_file)

                _, big_query_list = converter.convert(
                    entry.path, TYPES_MAP_PATH, None)
                self.assertEqual(bigquery_data, big_query_list,
                                 msg=f"\nFAILED AT FOLLOWING SCHEMA: {table_name}")

    def test_output_field_mappings_case(self):
        """
        Test if the converted schema is correct when providing a custom field type mapping.
        The custom map is provided via CLI with the '-f', '--extra-field-mappings' option.
        """
        for entry in os.scandir(TEST_DATA_PATH):
            if entry.name.endswith(".sql") and entry.name.startswith('field_mappings_'):
                table_name = entry.name.split(".")[0]

                # Find the corresponding .json file for the .sql input
                big_query_json = TEST_DATA_PATH + table_name + ".json"
                with open(big_query_json) as json_file:
                    bigquery_data = json.load(json_file)

                _, big_query_list = converter.convert(
                    entry.path, None, FIELD_MAP_PATH)
                self.assertEqual(bigquery_data, big_query_list,
                                 msg=f"\nFAILED AT FOLLOWING SCHEMA: {table_name}")

    @unittest.expectedFailure
    def test_invalid_sql_provided(self):
        """
        Test if the converter fails when provided with an .sql file missing the CREATE TABLE statement.
        """
        for entry in os.scandir(TEST_DATA_PATH):
            if entry.name.endswith(".sql") and entry.name.startswith('invalid'):
                _, big_query_list = converter.convert(entry.path, None, None)

    @unittest.expectedFailure
    def test_invalid_type_mappings_provided(self):
        """
        Test if the converter fails when provided with an invalid data type in the custom type map.
        It refers to the map passed with '--extra-type-mappings'.
        """
        for entry in os.scandir(TEST_DATA_PATH):
            if entry.name.endswith(".sql") and entry.name.startswith('type_mappings_'):
                _, big_query_list = converter.convert(
                    entry.path, INVALID_TYPES_MAP_PATH, None)

                invalid_types = list(
                    filter(lambda x: x['type'] not in BIGQUERY_TYPES, big_query_list))
                if len(invalid_types) > 0:
                    raise ValueError(
                        f'The provided data types are not valid in BigQuery: \n{invalid_types}\n')

    @unittest.expectedFailure
    def test_invalid_field_mappings_provided(self):
        """
        Test if the converter fails when provided with an invalid data type in the custom field map.
        It refers to the map passed with '--extra-field-mappings'.
        """
        for entry in os.scandir(TEST_DATA_PATH):
            if entry.name.endswith(".sql") and entry.name.startswith('field_mappings_'):
                _, big_query_list = converter.convert(
                    entry.path, None, INVALID_FIELDS_MAP_PATH)

                invalid_types = list(
                    filter(lambda x: x['type'] not in BIGQUERY_TYPES, big_query_list))
                if len(invalid_types) > 0:
                    raise ValueError(
                        f'The provided data types are not valid in BigQuery: \n{invalid_types}\n')


if __name__ == '__main__':
    unittest.main()
