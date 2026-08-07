from argparse import ArgumentParser
from json import dumps as json_dumps
from pathlib import Path

from .converter import convert


def main():
    parser = ArgumentParser(description="Convert mysql schemas to bigquery")
    parser.add_argument("path", type=Path, help="Path to .sql file to convert")
    parser.add_argument(
        "-o",
        "--output-path",
        type=Path,
        action="store",
        help="File path where to store the converted .json schema. "
        "By default the schema is printed to stdout.",
    )
    parser.add_argument(
        "-t",
        "--extra-type-mappings",
        action="store",
        help="Path to a .json file used to extend and/or override type mappings.",
    )
    parser.add_argument(
        "-f",
        "--extra-field-mappings",
        action="store",
        help="Path to a .json file used to assign a type to a specific field.",
    )
    parser.add_argument(
        "-d",
        "--drop-virtual-fields",
        action="store_true",
        help="The generated .json file will not contain VIRTUAL fields.",
    )

    args = parser.parse_args()

    _, big_query_list = convert(
        args.path,
        args.extra_type_mappings,
        args.extra_field_mappings,
        args.drop_virtual_fields,
    )

    data = json_dumps(big_query_list, indent=4)

    if args.output_path is None:
        print(data)

    else:
        args.output_path.write_text(data, encoding="utf-8")


if __name__ == "__main__":
    main()
