import csv
import argparse
import io
from sys import stderr

from typing import List, Text


EXPECTED_FIELDS = {"good_name", "cost", "quantity"}

def file_from_arguments() -> io.TextIOWrapper:
    parser = argparse.ArgumentParser(description="Demo project")
    parser.add_argument(
        "-i",
        type=argparse.FileType('r'),
        help="Path to csv file"
        )
    return parser.parse_args().i

def check_expected_fields(head: List[Text]):
    if not EXPECTED_FIELDS.issubset(head):
        bad_fields = EXPECTED_FIELDS - set(head)
        raise ValueError(f"No fields ({', '.join(bad_fields)}) in input file")

if __name__ == "__main__":
    with file_from_arguments() as csvfile:
        reader = csv.reader(csvfile)
        head_row = next(reader)
        check_expected_fields(head_row)

        index_by_name = {name: index for index, name in enumerate(head_row)}
        goods = {}

        for row in reader:
            try:
                name = row[index_by_name["good_name"]]
                cost = float(row[index_by_name["cost"]])
                quantity = int(row[index_by_name["quantity"]])
            except ValueError as val_err:
                print(val_err, file=stderr)
                continue

            if name in goods:
                goods[name]["total_cost"] += cost * quantity
                goods[name]["total_quantity"] += quantity
            else:
                goods[name] = {
                    "total_cost": cost * quantity,
                    "total_quantity": quantity
                }

        print("good_name, total_cost, total_quantity")
        for name in goods:
            print(name, goods[name]["total_cost"], goods[name]["total_quantity"], sep=', ')
