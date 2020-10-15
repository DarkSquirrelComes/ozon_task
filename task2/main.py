import csv
import argparse
import io
from sys import stderr

from collections import defaultdict

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

def print_goods(goods: defaultdict):
    print("good_name,total_cost,total_quantity")
    for name in goods:
        print(name, goods[name]["total_cost"], goods[name]["total_quantity"], sep=',')

if __name__ == "__main__":
    with file_from_arguments() as csvfile:
        reader = csv.DictReader(csvfile)

        goods = defaultdict(lambda: {
                    "total_cost": 0,
                    "total_quantity": 0
                })

        for row in reader:
            try:
                name = row["good_name"]
                cost = float(row["cost"])
                quantity = int(row["quantity"])
            except ValueError as val_err:
                print(val_err, file=stderr)
                continue

            goods[name]["total_cost"] += cost * quantity
            goods[name]["total_quantity"] += quantity

        print_goods(goods)
