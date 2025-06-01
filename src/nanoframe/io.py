# nanoframe/io.py

import csv
import json
from typing import List, Dict, Optional, Union, TextIO
from nanoframe.frame import NanoFrame
from nanoframe.exceptions import InvalidFileFormatError

__all__ = ['read_csv', 'to_csv', 'read_json', 'to_json']


def read_csv(
    file: Union[str, TextIO],
    delimiter: str = ",",
    header: bool = True,
    encoding: str = "utf-8"
) -> NanoFrame:
    """
    Read a CSV file and return a NanoFrame.

    :param file: Path to CSV file or file-like object.
    :param delimiter: Field delimiter.
    :param header: Whether the CSV has a header row.
    :param encoding: Encoding of the file.
    :return: NanoFrame object.
    """
    if isinstance(file, str):
        f = open(file, mode="r", encoding=encoding)
        should_close = True
    else:
        f = file
        should_close = False

    try:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

        if not rows:
            raise InvalidFileFormatError("CSV file is empty.")

        if header:
            columns = rows[0]
            data_rows = rows[1:]
        else:
            num_cols = len(rows[0])
            columns = [f"col{i}" for i in range(num_cols)]
            data_rows = rows

        # Transpose rows to columns
        col_data = {col: [] for col in columns}
        for row in data_rows:
            for col, value in zip(columns, row):
                col_data[col].append(_parse_value(value))

        return NanoFrame(col_data)

    finally:
        if should_close:
            f.close()


def to_csv(
    frame: NanoFrame,
    file: Union[str, TextIO],
    delimiter: str = ",",
    include_header: bool = True,
    encoding: str = "utf-8"
) -> None:
    """
    Write a NanoFrame to a CSV file.

    :param frame: NanoFrame object to write.
    :param file: Path or file-like object to write to.
    :param delimiter: Field delimiter.
    :param include_header: Whether to write header row.
    :param encoding: File encoding.
    """
    if isinstance(file, str):
        f = open(file, mode="w", encoding=encoding, newline="")
        should_close = True
    else:
        f = file
        should_close = False

    try:
        writer = csv.writer(f, delimiter=delimiter)
        columns = list(frame.columns.keys())
        if include_header:
            writer.writerow(columns)

        row_count = frame.row_count
        for i in range(row_count):
            row = [frame.columns[col][i] for col in columns]
            writer.writerow(row)

    finally:
        if should_close:
            f.close()


def read_json(
    file: Union[str, TextIO],
    encoding: str = "utf-8"
) -> NanoFrame:
    """
    Read a JSON file and return a NanoFrame.
    Supports list of records (list[dict]) format.

    :param file: Path or file-like object.
    :param encoding: File encoding.
    :return: NanoFrame object.
    """
    if isinstance(file, str):
        f = open(file, mode="r", encoding=encoding)
        should_close = True
    else:
        f = file
        should_close = False

    try:
        data = json.load(f)
        if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
            raise InvalidFileFormatError("JSON must be a list of dictionaries.")
        return NanoFrame(data)

    finally:
        if should_close:
            f.close()


def to_json(
    frame: NanoFrame,
    file: Union[str, TextIO],
    indent: Optional[int] = 4,
    encoding: str = "utf-8"
) -> None:
    """
    Write a NanoFrame to a JSON file (records format).

    :param frame: NanoFrame object.
    :param file: Path or file-like object.
    :param indent: JSON indent spacing.
    :param encoding: File encoding.
    """
    if isinstance(file, str):
        f = open(file, mode="w", encoding=encoding)
        should_close = True
    else:
        f = file
        should_close = False

    try:
        records = [
            {col: frame.columns[col][i] for col in frame.columns}
            for i in range(frame.row_count)
        ]
        json.dump(records, f, indent=indent)

    finally:
        if should_close:
            f.close()


def _parse_value(val: str) -> Union[str, int, float, None]:
    """Try to convert string to int, float, or keep as string."""
    val = val.strip()
    if val == "":
        return None
    try:
        if "." in val:
            return float(val)
        else:
            return int(val)
    except ValueError:
        return val