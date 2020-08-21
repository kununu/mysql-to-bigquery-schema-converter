# mysql-to-bigquery-schema-converter

A python script that converts a **mysql** schema to a **json** file to be consumed by Google Big Query.

The main logic is contained in `converter.py`.
For instruction on how to use the program, excecute: 

`$ python converter.py -h` 

Folder `test_data` is used for testing purposes.
In order to compare two files, they have to have the same name, e.g.:
`example_table.sql` and `example_table.json`.
