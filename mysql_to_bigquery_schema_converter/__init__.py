#!/usr/bin/env python

from mysql_to_bigquery_schema_converter.utils.bigquery_types_config import BIGQUERY_TYPES
import os
import json

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
