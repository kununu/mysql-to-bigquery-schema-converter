import autopep8
import json
import sys


def convert(filepath):
    CREATE_TABLE = 'CREATE TABLE'

    # TODO: move LUT in an external file
    data_type_LUT = {"char": "STRING",
                     "varchar": "STRING",
                     "text": "STRING",
                     "datetime": "STRING",
                     "timestamp": "TIMESTAMP",
                     "date": "STRING",
                     "time": "STRING",
                     "enum": "STRING",
                     "set": "STRING",
                     "int": "INTEGER",
                     "tinyint": "INTEGER",
                     "mediumint": "INTEGER",
                     "bigint": "INTEGER",
                     "float": "FLOAT",
                     "double": "FLOAT"
                     }

    table_name = None

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

            tmp_col_and_type = {"type": cleaned_type, "name": tmp_col_name}
            big_query_list.append(tmp_col_and_type)

            line = fp.readline()

        if table_name is None:
            raise ValueError(
                f'File {filepath} does not contain a CREATE TABLE STATEMENT')

    return table_name, big_query_list
    # TODO:
    # By default, on BQ Column allows NULL. Change mode to required for
    # not-NULL fields.


if __name__ == "__main__":
    filepath = sys.argv[1]
    table_name, big_query_list = convert(filepath)

    with open(f'{table_name}.json', 'w') as outfile:
        json.dump(big_query_list, outfile, indent=4)
