import inspect

# [top]
from df_base import DF
from util import dict_match

class DfRow(DF):
    def __init__(self, rows):
        assert len(rows) > 0
        assert all(dict_match(r, rows[0]) for r in rows)
        self._data = rows
    # [/top]

    # [simple]
    def ncol(self):
        return len(self._data[0].keys())

    def nrow(self):
        return len(self._data)

    def cols(self):
        return set(self._data[0].keys())
    # [/simple]

    def eq(self, other):
        assert isinstance(other, DF)
        for (i, row) in enumerate(self._data):
            for key in row:
                if key not in other.cols():
                    return False
                if row[key] != other.get(key, i):
                    return False
        return True

    def get(self, col, row):
        assert col in self._data[0]
        assert 0 <= row < len(self._data)
        return self._data[row][col]

    # [select]
    def select(self, *names):
        assert all(n in self._data[0] for n in names)
        rows = [{key: r[key] for key in names} for r in self._data]
        return DfRow(rows)
    # [/select]

    # [filter]
    def filter(self, func):
        params = list(inspect.signature(func).parameters.keys())
        result = [r for r in self._data if func(**r)]
        return DfRow(result)
    # [/filter]

    def __str__(self):
        return str(self._data)
