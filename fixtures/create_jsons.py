import os
import sys
import csv
import json
from typing import Callable

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_csv2dict_str(filename: str) -> list[dict]:
    """
    reads csv and puts it to a list of dictionary of strings
    """

    try:
        json_dict = []
        with open(filename, "r", encoding="utf-8", newline='') as file:
            contents = csv.DictReader(file, delimiter=',')
            for row in contents:
                json_dict.append(row)
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)
    return json_dict


def parse_ads(data: list[dict]) -> list[dict]:
    """
    parses ads columns into correct data types
    """
    try:
        return [
            {
                "model": "ads.ads",
                "pk": int(item["Id"]),
                "fields": {
                    "name": item["name"],
                    "author": item["author"],
                    "price": int(item["price"]),
                    "description": item["description"],
                    "address": item["address"],
                    "is_published": True if (item["is_published"]) == 'TRUE' else False
                }
            }
            for item in data
        ]
    except KeyError as error:
        print(error)
        sys.exit(1)


def parse_category(data: list[dict]) -> list[dict]:
    """
    parses category columns into correct data types
    """
    try:
        return [
            {
                "model": "ads.cat",
                "pk": int(item["id"]),
                "fields": {
                    "name": item["name"],
                }
            }
            for item in data
        ]
    except KeyError as error:
        print(error)
        sys.exit(1)


def csv2json(filename: str, func: Callable) -> None:
    """
    reads a csv file with 'filename', parses it using 'func' and writes into a JSON file
    """

    data = func(read_csv2dict_str(os.path.join(BASE_DIR, filename)))
    try:
        with open(filename[:filename.rfind(".")] + ".json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent='\t', ensure_ascii=False)
    except Exception as error:
        print(error)
        sys.exit(2)


if __name__ == "__main__":
    # writing from CSVs to JSONs
    csv2json("ads.csv", parse_ads)
    csv2json("categories.csv", parse_category)

    # with open("datasets/ads.json", "r", encoding="utf-8") as f:
    #     temp = json.load(f)
    # print(*temp[0].items(), sep='\n')
