#!/usr/bin/env python

import unittest
import converter


class TestConverter(unittest.TestCase):
    DATA_DIR = "./test_cases"

    def get_contents(self, file_name):
        with open(file_name, 'r') as f:
            return f.read()

    def test_sample_table(self):
        table_name, schema_string = converter.convert(
            f"{self.DATA_DIR}/sample_table.sql")

        self.assertEqual(table_name, "sample_table")
        self.assertEqual(schema_string, self.get_contents(
            f"{self.DATA_DIR}/sample_table.json"))

    def test_complex_table(self):
        table_name, schema_string = converter.convert(
            f"{self.DATA_DIR}/complex_table.sql")

        self.assertEqual(table_name, "complex_table")
        self.assertEqual(schema_string, self.get_contents(
            f"{self.DATA_DIR}/complex_table.json"))

    def test_missing_table_data(self):
        with self.assertRaises(Exception) as raised:
            converter.convert(f"{self.DATA_DIR}/missing_table.sql")
            self.assertEqual(str(raised.exception),
                             "Invalid MySQL source schema.")

    def test_invalid_column_type(self):
        with self.assertRaises(Exception) as raised:
            converter.convert(f"{self.DATA_DIR}/invalid_column_type.sql")
            self.assertEqual(str(
                raised.exception), "Invalid column type found: `my_special_type` is not a valid MySQL data type.")

    def test_valid_field_mapping(self):
        table_name, schema_string = converter.convert(
            f"{self.DATA_DIR}/sample_table.sql",
            extra_field_mappings=f"{self.DATA_DIR}/valid_field_mappings.json")

        self.assertEqual(table_name, "sample_table")
        self.assertEqual(schema_string, self.get_contents(
            f"{self.DATA_DIR}/sample_table_with_field_mappings.json"))

    def test_valid_type_mapping(self):
        table_name, schema_string = converter.convert(
            f"{self.DATA_DIR}/sample_table.sql",
            extra_type_mappings=f"{self.DATA_DIR}/valid_type_mappings.json")

        self.assertEqual(table_name, "sample_table")
        self.assertEqual(schema_string, self.get_contents(
            f"{self.DATA_DIR}/sample_table_with_type_mappings.json"))

    def test_invalid_field_mapping(self):
        with self.assertRaises(Exception) as raised:
            converter.convert(f"{self.DATA_DIR}/sample_table.sql",
                              extra_field_mappings=f"{self.DATA_DIR}/invalid_field_mappings.json")
            self.assertEqual(str(
                raised.exception), "Invalid field mapping found: `NOT_A_VALID_TYPE` is not a valid BigQuery data type.")

    def test_missing_field_mapping(self):
        with self.assertRaises(Exception) as raised:
            converter.convert(f"{self.DATA_DIR}/sample_table.sql",
                              extra_field_mappings=f"{self.DATA_DIR}/missing_field_mappings.json")
            self.assertEqual(str(
                raised.exception), "Mapping field not found: `some_non_existing_field` does not occure in source schema.")

    def test_invalid_type_mapping(self):
        with self.assertRaises(Exception) as raised:
            converter.convert(f"{self.DATA_DIR}/sample_table.sql",
                              extra_type_mappings=f"{self.DATA_DIR}/invalid_type_mappings.json")
            self.assertEqual(str(
                raised.exception), "Invalid type mapping found: `NOT_A_VALID_TYPE` is not a valid BigQuery data type.")


if __name__ == "__main__":
    unittest.main()
