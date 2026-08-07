from json import loads as json_loads
from pathlib import Path

BIGQUERY_TYPES = {
    "BIGNUMERIC",
    "BOOL",
    "BOOLEAN",
    "BYTES",
    "DATE",
    "DATETIME",
    "FLOAT",
    "FLOAT64",
    "GEOGRAPHY",
    "INT64",
    "INTEGER",
    "INTERVAL",
    "JSON",
    "NUMERIC",
    "RANGE",
    "RECORD",
    "STRING",
    "STRUCT",
    "TIME",
    "TIMESTAMP",
}

PACKAGE_DIR = Path(__file__).parent

DATA_TYPE_LUT = PACKAGE_DIR / "types_map.json"


def fetch_lookup_table(filepath):
    return json_loads(Path(filepath).read_bytes())


def check_if_required(line):
    return "NOT NULL" in line


def parse_table_name(line):
    # take everything after 'CREATE TABLE', skipping an optional 'IF NOT EXISTS'
    rest = line.split("CREATE TABLE", 1)[1].strip()
    if rest.upper().startswith("IF NOT EXISTS"):
        rest = rest[len("IF NOT EXISTS") :].strip()

    return rest.split()[0].replace("`", "").rstrip("(")


def convert(
    filepath,
    extra_type_mappings,
    extra_field_mappings,
    drop_virtual_fields=False,
):
    CREATE_TABLE = "CREATE TABLE"
    VIRTUAL_COLUMN = ") VIRTUAL"
    table_name = None
    field_to_type_map = {}

    data_type_LUT = fetch_lookup_table(DATA_TYPE_LUT)

    if extra_type_mappings is not None:
        extended_type_map = fetch_lookup_table(extra_type_mappings)
        data_type_LUT = {**data_type_LUT, **extended_type_map}

    # data types are matched case-insensitively
    data_type_LUT = {key.lower(): value for key, value in data_type_LUT.items()}

    if extra_field_mappings is not None:
        field_to_type_map = fetch_lookup_table(extra_field_mappings)

    # Create a list of dict from which generate .json file
    big_query_list = []

    # open .sql file with table creation statement
    with open(filepath, encoding="utf-8") as fp:
        line = fp.readline()

        while line:
            # find table name and save it in a variable
            if table_name is None:
                if CREATE_TABLE in line:
                    table_name = parse_table_name(line)
                    line = fp.readline()
                    continue

                line = fp.readline()
                continue

            if VIRTUAL_COLUMN in line and drop_virtual_fields:
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

            tmp_col_name = tmp_col_name.replace("`", "")

            # Remove trailing comma if present, take all chars till `(`
            cleaned_type = tmp_line[1].rstrip(",").split("(")[0]

            try:
                # find corresponing data type in BQ
                cleaned_type = data_type_LUT[cleaned_type.lower()]
            except KeyError:
                print(f"No match found for the following data type: {cleaned_type}\n")
                raise

            if tmp_col_name in field_to_type_map:
                cleaned_type = field_to_type_map[tmp_col_name]

            tmp_col_and_type = {"type": cleaned_type, "name": tmp_col_name}

            if is_field_required:
                tmp_col_and_type["mode"] = "REQUIRED"
            else:
                tmp_col_and_type["mode"] = "NULLABLE"

            big_query_list.append(tmp_col_and_type)

            line = fp.readline()

        if table_name is None:
            raise ValueError(
                f"File {filepath} does not contain a CREATE TABLE STATEMENT"
            )

    # Check if the generated output has valid bigquery data types
    invalid_types = list(
        filter(lambda x: x["type"] not in BIGQUERY_TYPES, big_query_list)
    )
    if len(invalid_types) > 0:
        raise ValueError(
            f"The provided data types are not valid in BigQuery: \n{invalid_types}\n"
        )

    return table_name, big_query_list
