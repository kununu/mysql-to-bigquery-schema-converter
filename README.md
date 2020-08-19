# mysql-to-bigquery-schema-converter

A python script that converts a **mysql** schema to a **json** file to be consumed by Google Big Query.

The main logic is contained in `converter.py`.
To manually run, excecute: `python converter.py <path/to/mysql_schema.sql>` 

Folders `test_data_sql` and `test_data_bigquery` are used for testing purposes.
In order to compare two files, they have to have the same name, e.g.:
`example_table.sql` and `example_table.json`.
