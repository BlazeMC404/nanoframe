# nanoframe/frame.py

from typing import Any, List, Dict, Union, Optional, Callable
from copy import deepcopy
from collections import OrderedDict
from nanoframe.exceptions import ColumnNotFoundError, RowIndexError
from nanoframe.utils import infer_dtype, format_table


class NanoFrame:
    def __init__(self, data: Union[List[Dict[str, Any]], Dict[str, List[Any]]]):
        if isinstance(data, dict):
            self.columns = OrderedDict(data)
        elif isinstance(data, list):
            self.columns = self._from_records(data)
        else:
            raise TypeError("NanoFrame accepts either a list of dicts or dict of lists")

        self._validate_columns()
        self.shape = (self.row_count, self.column_count)
        self.dtypes = {col: infer_dtype(vals) for col, vals in self.columns.items()}

    def _from_records(self, records: List[Dict[str, Any]]) -> OrderedDict:
        columns = OrderedDict()
        for record in records:
            for key, value in record.items():
                if key not in columns:
                    columns[key] = []
                columns[key].append(value)
        return columns

    def _validate_columns(self):
        lengths = {len(col) for col in self.columns.values()}
        if len(lengths) > 1:
            raise ValueError("All columns must have the same length")

    @property
    def row_count(self) -> int:
        return len(next(iter(self.columns.values()), []))

    @property
    def column_count(self) -> int:
        return len(self.columns)

    def head(self, n: int = 5) -> 'NanoFrame':
        return self._subset(slice(0, n))

    def tail(self, n: int = 5) -> 'NanoFrame':
        return self._subset(slice(-n, None))

    def _subset(self, row_slice: slice) -> 'NanoFrame':
        sub_columns = {col: vals[row_slice] for col, vals in self.columns.items()}
        return NanoFrame(sub_columns)

    def select(self, cols: List[str]) -> 'NanoFrame':
        missing = [col for col in cols if col not in self.columns]
        if missing:
            raise ColumnNotFoundError(f"Columns not found: {missing}")
        return NanoFrame({col: deepcopy(self.columns[col]) for col in cols})

    def drop(self, cols: List[str]) -> 'NanoFrame':
        keep = [col for col in self.columns if col not in cols]
        return self.select(keep)

    def filter(self, condition: Callable[[Dict[str, Any]], bool]) -> 'NanoFrame':
        indices = [
            i for i in range(self.row_count)
            if condition({col: self.columns[col][i] for col in self.columns})
        ]
        return self._subset(indices)

    def __getitem__(self, key: Union[str, List[str]]) -> Union[List[Any], 'NanoFrame']:
        if isinstance(key, str):
            if key not in self.columns:
                raise ColumnNotFoundError(f"Column '{key}' does not exist")
            return self.columns[key]
        elif isinstance(key, list):
            return self.select(key)
        else:
            raise TypeError("Key must be a column name or list of column names")

    def __setitem__(self, key: str, value: List[Any]) -> None:
        if len(value) != self.row_count:
            raise ValueError("Length of new column must match number of rows")
        self.columns[key] = value
        self.dtypes[key] = infer_dtype(value)

    def loc(self, index: int) -> Dict[str, Any]:
        if not (0 <= index < self.row_count):
            raise RowIndexError(f"Row index {index} out of bounds")
        return {col: self.columns[col][index] for col in self.columns}

    def apply(self, func: Callable[[Any], Any], columns: Optional[List[str]] = None) -> None:
        target_cols = columns if columns else list(self.columns.keys())
        for col in target_cols:
            self.columns[col] = [func(val) for val in self.columns[col]]

    def rename(self, mapping: Dict[str, str]) -> None:
        for old, new in mapping.items():
            if old not in self.columns:
                raise ColumnNotFoundError(f"Column '{old}' not found")
            self.columns[new] = self.columns.pop(old)
            self.dtypes[new] = self.dtypes.pop(old)

    def to_dict(self) -> Dict[str, List[Any]]:
        return deepcopy(self.columns)

    def __repr__(self) -> str:
        return format_table(self.columns, max_rows=10)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NanoFrame):
            return False
        return self.columns == other.columns

    def describe(self) -> 'NanoFrame':
        numeric_cols = {
            k: v for k, v in self.columns.items()
            if all(isinstance(x, (int, float)) for x in v)
        }
        desc = OrderedDict()
        for col, values in numeric_cols.items():
            desc[col] = [
                len(values),
                sum(values) / len(values) if values else 0,
                min(values) if values else None,
                max(values) if values else None
            ]
        return NanoFrame({
            "stat": ["count", "mean", "min", "max"],
            **desc
        })