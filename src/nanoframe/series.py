# nanoframe/series.py

from typing import Any, List, Union, Callable, Optional
from nanoframe.utils import infer_dtype


class NanoSeries:
    def __init__(self, data: List[Any], name: Optional[str] = None, index: Optional[List[Any]] = None):
        self.data = data
        self.name = name
        self.index = index if index else list(range(len(data)))
        if len(self.index) != len(self.data):
            raise ValueError("Length of index must match length of data")
        self.dtype = infer_dtype(data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, key: Union[int, slice, Any]) -> Any:
        if isinstance(key, (int, slice)):
            return NanoSeries(self.data[key], self.name, self.index[key]) if isinstance(key, slice) else self.data[key]
        elif key in self.index:
            idx = self.index.index(key)
            return self.data[idx]
        else:
            raise KeyError(f"Index '{key}' not found")

    def __setitem__(self, key: Union[int, Any], value: Any):
        if isinstance(key, int):
            self.data[key] = value
        elif key in self.index:
            idx = self.index.index(key)
            self.data[idx] = value
        else:
            raise KeyError(f"Index '{key}' not found")

    def __repr__(self) -> str:
        lines = []
        for idx, val in zip(self.index, self.data):
            lines.append(f"{idx}: {val}")
        header = f"<NanoSeries: '{self.name}' dtype={self.dtype}>"
        return f"{header}\n" + "\n".join(lines)

    def apply(self, func: Callable[[Any], Any]) -> 'NanoSeries':
        return NanoSeries([func(x) for x in self.data], self.name, self.index)

    def map(self, mapping: dict) -> 'NanoSeries':
        return self.apply(lambda x: mapping.get(x, x))

    def to_list(self) -> List[Any]:
        return self.data.copy()

    def to_dict(self) -> dict:
        return dict(zip(self.index, self.data))

    def mean(self) -> float:
        numeric = [x for x in self.data if isinstance(x, (int, float))]
        return sum(numeric) / len(numeric) if numeric else float('nan')

    def min(self) -> Any:
        return min(self.data)

    def max(self) -> Any:
        return max(self.data)

    def sum(self) -> Any:
        return sum(self.data)

    def unique(self) -> List[Any]:
        seen = set()
        return [x for x in self.data if not (x in seen or seen.add(x))]

    def value_counts(self) -> dict:
        from collections import Counter
        return dict(Counter(self.data))

    def sort_values(self, reverse=False) -> 'NanoSeries':
        sorted_data = sorted(zip(self.data, self.index), reverse=reverse)
        data, index = zip(*sorted_data)
        return NanoSeries(list(data), self.name, list(index))

    def isnull(self) -> 'NanoSeries':
        return NanoSeries([x is None for x in self.data], name=f"{self.name}_isnull", index=self.index)

    def notnull(self) -> 'NanoSeries':
        return NanoSeries([x is not None for x in self.data], name=f"{self.name}_notnull", index=self.index)

    def __eq__(self, other: Any) -> 'NanoSeries':
        if isinstance(other, NanoSeries):
            if self.index != other.index:
                raise ValueError("Cannot compare NanoSeries with different indexes")
            return NanoSeries([a == b for a, b in zip(self.data, other.data)], name=f"{self.name}_eq", index=self.index)
        else:
            return NanoSeries([x == other for x in self.data], name=f"{self.name}_eq", index=self.index)

    def __add__(self, other: Union['NanoSeries', int, float]) -> 'NanoSeries':
        return self._binary_op(other, lambda a, b: a + b, 'add')

    def __sub__(self, other: Union['NanoSeries', int, float]) -> 'NanoSeries':
        return self._binary_op(other, lambda a, b: a - b, 'sub')

    def __mul__(self, other: Union['NanoSeries', int, float]) -> 'NanoSeries':
        return self._binary_op(other, lambda a, b: a * b, 'mul')

    def __truediv__(self, other: Union['NanoSeries', int, float]) -> 'NanoSeries':
        return self._binary_op(other, lambda a, b: a / b, 'div')

    def _binary_op(self, other, op, op_name: str) -> 'NanoSeries':
        if isinstance(other, NanoSeries):
            if self.index != other.index:
                raise ValueError("Indexes must match for binary operations")
            return NanoSeries([op(a, b) for a, b in zip(self.data, other.data)], name=f"{self.name}_{op_name}", index=self.index)
        elif isinstance(other, (int, float)):
            return NanoSeries([op(x, other) for x in self.data], name=f"{self.name}_{op_name}", index=self.index)
        else:
            raise TypeError(f"Unsupported operand type(s) for {op_name}: '{type(self).__name__}' and '{type(other).__name__}'")