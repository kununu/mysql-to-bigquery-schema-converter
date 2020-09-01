#!/usr/bin/env python

import json
import argparse
import mysql_to_bigquery_schema_converter as converter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert mysql schemas to bigquery')
    parser.add_argument('Path',
                        type=str,
                        help='Path to .sql file to convert')
    parser.add_argument('-o', '--output-path',
                        action='store',
                        help='Output path where to store the converted .json file. The file will be named after '
                        'the table name. E.g.: </output/path/>cool_table.json')
    parser.add_argument('-t', '--extra-type-mappings',
                        action='store',
                        help='Path to a .json file used to extend and/or override type mapping.')
    parser.add_argument('-f', '--extra-field-mappings',
                        action='store',
                        help='Path to a .json file used to assign a type to a spefic field.')

    args = parser.parse_args()
    filepath = args.Path
    output_path = args.output_path
    extra_type_mappings = args.extra_type_mappings
    extra_field_mappings = args.extra_field_mappings

    table_name, big_query_list = converter.convert(
        filepath, extra_type_mappings, extra_field_mappings)

    if output_path is None:
        print(f'\nSchema processed for table: {table_name}\n')
        print(json.dumps(big_query_list, indent=4))
    else:
        with open(f'{output_path}/{table_name}.json', 'w') as outfile:
            json.dump(big_query_list, outfile, indent=4)
