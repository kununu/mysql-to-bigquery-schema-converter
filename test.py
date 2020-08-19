import unittest
import converter
import json
import os


class TestConverter(unittest.TestCase):
    def test_output_correctly_generated(self):
        """
        Test if converted mysql schema matches with the BigQuery json one.
        Loop through two input folders. `.sql` and `.json` files must have 
        the same name in order to be compared.
        """
        mysql_path = "test_data_sql/"
        bigquery_path = "test_data_bigquery/"

        for entry in os.scandir(mysql_path):
            if entry.name.endswith(".sql"):
                table_name = entry.name.split(".")[0]

                # Find the corresponding .json file for the .sql input
                big_query_json = bigquery_path + table_name + ".json"
                with open(big_query_json) as json_file:
                    bigquery_data = json.load(json_file)

                _, big_query_list = converter.convert(entry.path)
                self.assertEqual(bigquery_data, big_query_list)


if __name__ == '__main__':
    unittest.main()
