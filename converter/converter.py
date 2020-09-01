#!/usr/bin/env python

import json
import argparse
from utils.bigquery_types_config import BIGQUERY_TYPES
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_TYPE_LUT = dir_path + '/types_map.json'


def fetch_lookup_table(filepath):

    with open(filepath) as json_file:
        lookup_table = json.load(json_file)

    return lookup_table


def check_if_required(line):

    is_field_required = 'NOT NULL' in line
    return is_field_required


def convert(filepath, extra_type_mappings, extra_field_mappings):

    CREATE_TABLE = 'CREATE TABLE'
    table_name = None
    field_to_type_map = {}

    data_type_LUT = fetch_lookup_table(DATA_TYPE_LUT)

    if extra_type_mappings is not None:
        extened_type_map = fetch_lookup_table(extra_type_mappings)
        data_type_LUT = {**data_type_LUT, **extened_type_map}

    if extra_field_mappings is not None:
        field_to_type_map = fetch_lookup_table(extra_field_mappings)

    # Create a list of dict from which generate .json file
    big_query_list = []

    # open .sql file with table creation statement
    with open(filepath) as fp:
        line = fp.readline()

        while line:
            # find table name and save it in a variable
            if table_name is None:
                if CREATE_TABLE in line:
                    # get table name
                    table_name = line.split()[2]
                    # remove backticks
                    table_name = table_name.replace("`", "")
                    line = fp.readline()
                    continue
                line = fp.readline()
                continue

            # parse each line and check for column name and type
            # convert data type from mysql to bigquery using a Look Up Table
            is_field_required = check_if_required(line)
            tmp_line = line.split()
            tmp_col_name = tmp_line[0]

            if "`" not in tmp_col_name:
                # previous iteration had the last last column, quit
                break
            else:
                tmp_col_name = tmp_col_name.replace("`", "")

            # Take all chars till `(`
            cleaned_type = tmp_line[1].split("(")[0]

            try:
                # find corresponing data type in BQ
                cleaned_type = data_type_LUT[cleaned_type]
            except Exception as e:
                print(
                    f'No match found for the following data type: {cleaned_type}\n')
                raise

            if tmp_col_name in field_to_type_map:
                cleaned_type = field_to_type_map[tmp_col_name]

            tmp_col_and_type = {"type": cleaned_type, "name": tmp_col_name}

            if is_field_required:
                tmp_col_and_type["mode"] = 'REQUIRED'
            else:
                tmp_col_and_type["mode"] = 'NULLABLE'

            big_query_list.append(tmp_col_and_type)

            line = fp.readline()

        if table_name is None:
            raise ValueError(
                f'File {filepath} does not contain a CREATE TABLE STATEMENT')

    # Check if the generated output has valid bigquery data types
    invalid_types = list(
        filter(lambda x: x['type'] not in BIGQUERY_TYPES, big_query_list))
    if len(invalid_types) > 0:
        raise ValueError(
            f'The provided data types are not valid in BigQuery: \n{invalid_types}\n')

    return table_name, big_query_list


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

    table_name, big_query_list = convert(
        filepath, extra_type_mappings, extra_field_mappings)

    if output_path is None:
        print(f'\nSchema processed for table: {table_name}\n')
        print(json.dumps(big_query_list, indent=4))
    else:
        with open(f'{output_path}/{table_name}.json', 'w') as outfile:
            json.dump(big_query_list, outfile, indent=4)
