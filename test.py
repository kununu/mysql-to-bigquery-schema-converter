#!/usr/bin/env python

import unittest
import json
import mysql_to_bigquery_schema_converter as converter

TEST_DATA_PATH = "./test_data"
TYPES_MAP_PATH = TEST_DATA_PATH + "/type_mappings_map.json"
FIELD_MAP_PATH = TEST_DATA_PATH + "/field_mappings_map.json"
INVALID_TYPES_MAP_PATH = TEST_DATA_PATH + "/invalid_type_mappings_map.json"
INVALID_FIELDS_MAP_PATH = TEST_DATA_PATH + "/invalid_field_mappings_map.json"


class TestConverter(unittest.TestCase):
    maxDiff = None

    def test_output_correctly_generated_default(self):
        """
        Test if converted mysql schema matches with the BigQuery json one.
        """

        # Point to the default `.sql` case and its relative `.json`
        default_case_sql = TEST_DATA_PATH + "/default_case.sql"
        big_query_json = TEST_DATA_PATH + "/default_case.json"
        with open(big_query_json) as json_file:
            bigquery_data = json.load(json_file)

        _, big_query_list = converter.convert(default_case_sql, None, None)
        self.assertEqual(bigquery_data, big_query_list,
                         msg=f"\nFAILED AT FOLLOWING SCHEMA: {default_case_sql}")

    def test_output_type_mappings_case(self):
        """
        Test if the converted schema is correct when providing a custom data type mapping.
        The custom map is provided via CLI with the '-t', '--extra-type-mappings' option.
        """

        # Point to the type_mappings_case `.sql` case and its relative `.json`
        type_mappings_case_sql = TEST_DATA_PATH + "/type_mappings_case.sql"
        big_query_json = TEST_DATA_PATH + "/type_mappings_case.json"
        with open(big_query_json) as json_file:
            bigquery_data = json.load(json_file)

        _, big_query_list = converter.convert(
            type_mappings_case_sql, TYPES_MAP_PATH, None)
        self.assertEqual(bigquery_data, big_query_list,
                         msg=f"\nFAILED AT FOLLOWING SCHEMA: {type_mappings_case_sql}")

    def test_output_field_mappings_case(self):
        """
        Test if the converted schema is correct when providing a custom field type mapping.
        The custom map is provided via CLI with the '-f', '--extra-field-mappings' option.
        """

        # Point to the field_mappings_case `.sql` case and its relative `.json`
        field_mappings_case_sql = TEST_DATA_PATH + "/field_mappings_case.sql"
        big_query_json = TEST_DATA_PATH + "/field_mappings_case.json"
        with open(big_query_json) as json_file:
            bigquery_data = json.load(json_file)

        _, big_query_list = converter.convert(
            field_mappings_case_sql, None, FIELD_MAP_PATH)
        self.assertEqual(bigquery_data, big_query_list,
                         msg=f"\nFAILED AT FOLLOWING SCHEMA: {field_mappings_case_sql}")

    def test_invalid_sql_provided(self):
        """
        Test if the converter fails when provided with an .sql file missing the CREATE TABLE statement.
        """

        invalid_sql_case = TEST_DATA_PATH + "/invalid_sql_case.sql"
        with self.assertRaises(ValueError) as ctx:
            _, big_query_list = converter.convert(invalid_sql_case, None, None)

        expected = f"File {TEST_DATA_PATH}/invalid_sql_case.sql does not contain a CREATE TABLE STATEMENT"
        self.assertEqual(str(ctx.exception), expected)

    def test_invalid_type_mappings_provided(self):
        """
        Test if the converter fails when provided with an invalid data type in the custom type map.
        It refers to the map passed with '--extra-type-mappings'.
        """

        type_mappings_case = TEST_DATA_PATH + "/type_mappings_case.sql"
        with self.assertRaises(ValueError) as ctx:
            _, big_query_list = converter.convert(
                type_mappings_case, INVALID_TYPES_MAP_PATH, None)
        expected = "The provided data types are not valid in BigQuery: \n[{'type': 'sTRING', 'name': 'created_at', 'mode': 'REQUIRED'}]\n"
        self.assertEqual(str(ctx.exception), expected)

    def test_invalid_field_mappings_provided(self):
        """
        Test if the converter fails when provided with an invalid data type in the custom field map.
        It refers to the map passed with '--extra-field-mappings'.
        """

        field_mappings_case = TEST_DATA_PATH + "/field_mappings_case.sql"
        with self.assertRaises(ValueError) as ctx:
            _, big_query_list = converter.convert(
                field_mappings_case, None, INVALID_FIELDS_MAP_PATH)

        expected = "The provided data types are not valid in BigQuery: \n[{'type': 'sTRING', 'name': 'created_at', 'mode': 'REQUIRED'}]\n"
        self.assertEqual(str(ctx.exception), expected)


if __name__ == '__main__':
    unittest.main()
