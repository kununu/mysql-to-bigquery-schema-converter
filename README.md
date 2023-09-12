# MySQL to BigQuery Schema Converter

Convert MySQL schema (from a `.sql` file) into a BigQuery-compatible schema in JSON format.

## Features:
- Maps common MySQL data types to BigQuery types.
- Customize conversions with additional mappings.
- Option to handle and drop virtual fields in MySQL.

## Quick Start:

1. Ensure you have Python 3.9 or higher installed.
2. We use [`poetry`](https://python-poetry.org/) for dependency management. Ensure it's installed.
3. Clone this repository and navigate to the project directory.

### Using the Converter:

To convert a MySQL `.sql` schema to a BigQuery JSON schema, use the `convert.py` script:

```bash
poetry run  python convert.py <path_to_sql_file> [options]
```

#### Options:
* `-o`, `--output-path` : Specify the output path where the converted `.json` file should be stored. By default, the output will be printed to the console. If specified, the output file will be named after the table, e.g., `cool_table.json`.
* `-t`, `--extra-type-mappings` : Provide a path to a `.json` file to extend and/or override default type mappings.
* `-f`, `--extra-field-mappings` : Provide a path to a `.json` file to assign a specific type to a particular field.
* `-d`, `--drop-virtual-fields` : Set this flag to exclude virtual fields in the generated `.json` schema.


## Testing:

To validate the conversion, run the tests:

```
poetry run python test.py
```


The `test_data` folder contains test cases and their expected outputs.

## Custom Mappings:

The default MySQL to BigQuery type mappings are in `types_map.json`. If you need different mappings, you can use the `-t` (or `--extra-type-mappings`) and `-f` (or `--extra-field-mappings`) options.

## Contribution:

- For security vulnerabilities, see `SECURITY.md`.
- Pull requests and issues for improvements are welcome.

## License:
Licensed under the MIT License. Check out the [LICENSE](LICENSE) file.
