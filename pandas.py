import csv
import sqlite3

class Series:
    def __init__(self, data):
        self.data = list(data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __eq__(self, other):
        return Series([x == other for x in self.data])

    def sum(self):
        return sum(1 for x in self.data if x)

    @property
    def str(self):
        class _Str:
            def __init__(self, series):
                self.series = series

            def contains(self, pattern, case=False, na=False):
                res = []
                for val in self.series.data:
                    if val is None:
                        res.append(False if not na else None)
                        continue
                    text = str(val)
                    pat = pattern if case else pattern.lower()
                    source = text if case else text.lower()
                    res.append(pat in source)
                return Series(res)

        return _Str(self)

    def unique(self):
        seen = []
        for item in self.data:
            if item not in seen and item is not None:
                seen.append(item)
        return seen


class DataFrame:
    def __init__(self, data):
        if isinstance(data, dict):
            self._columns = list(data.keys())
            length = len(next(iter(data.values()), []))
            self._data = []
            for i in range(length):
                row = {col: data[col][i] for col in self._columns}
                self._data.append(row)
        elif isinstance(data, list):
            self._data = data
            self._columns = list(data[0].keys()) if data else []
        else:
            raise TypeError("Unsupported data type for DataFrame")

    @property
    def columns(self):
        return list(self._columns)

    @property
    def shape(self):
        return (len(self._data), len(self._columns))

    def head(self, n=5):
        return DataFrame(self._data[:n])

    def dropna(self):
        new = [row for row in self._data if all(row[c] is not None for c in self._columns)]
        return DataFrame(new)

    def isnull(self):
        class NullCounter:
            def __init__(self, df):
                self.df = df

            def sum(self):
                counts = {}
                for col in self.df._columns:
                    counts[col] = sum(row[col] is None for row in self.df._data)
                class Total:
                    def __init__(self, counts):
                        self.counts = counts
                    def sum(self):
                        return sum(self.counts.values())
                return Total(counts)
        return NullCounter(self)

    def duplicated(self):
        seen = set()
        flags = []
        for row in self._data:
            t = tuple(row[c] for c in self._columns)
            if t in seen:
                flags.append(True)
            else:
                seen.add(t)
                flags.append(False)
        return Series(flags)

    def drop_duplicates(self):
        seen = set()
        new = []
        for row in self._data:
            t = tuple(row[c] for c in self._columns)
            if t not in seen:
                seen.add(t)
                new.append(row)
        return DataFrame(new)

    @property
    def dtypes(self):
        types = {}
        for col in self._columns:
            val = None
            for row in self._data:
                if row[col] is not None:
                    val = row[col]
                    break
            types[col] = type(val).__name__ if val is not None else 'object'
        return types

    def to_csv(self, index=False):
        output = ",".join(self._columns) + "\n"
        for row in self._data:
            values = ["" if row[c] is None else str(row[c]) for c in self._columns]
            output += ",".join(values) + "\n"
        return output

    def to_excel(self, *a, **k):
        return None

    def to_sql(self, table_name, conn, if_exists="fail", index=False):
        cur = conn.cursor()
        if if_exists == "replace":
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cols_sql = ", ".join(f"{c} TEXT" for c in self._columns)
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_sql})")
        for row in self._data:
            cur.execute(
                f"INSERT INTO {table_name} ({', '.join(self._columns)}) VALUES ({', '.join('?' for _ in self._columns)})",
                [row.get(c) for c in self._columns],
            )
        conn.commit()

    @property
    def iloc(self):
        class _ILoc:
            def __init__(self, data):
                self.data = data
            def __getitem__(self, idx):
                return self.data[idx]
        return _ILoc(self._data)

    def __getitem__(self, key):
        if isinstance(key, str):
            return Series([row.get(key) for row in self._data])
        elif isinstance(key, list):
            return DataFrame([{k: row.get(k) for k in key} for row in self._data])
        elif isinstance(key, Series):
            return DataFrame([row for row, flag in zip(self._data, key.data) if flag])
        elif isinstance(key, list) and all(isinstance(k, bool) for k in key):
            return DataFrame([row for row, flag in zip(self._data, key) if flag])
        else:
            raise KeyError(key)

    @property
    def empty(self):
        return len(self._data) == 0


class ExcelWriter:
    def __init__(self, *a, **k):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass


def read_csv(file_like):
    if hasattr(file_like, "read"):
        content = file_like.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        lines = content.splitlines()
        reader = csv.DictReader(lines)
    else:
        with open(file_like, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
    rows = []
    for row in reader:
        cleaned = {k: (v if v != "" else None) for k, v in row.items()}
        rows.append(cleaned)
    return DataFrame(rows)


def read_sql_query(query, conn):
    cur = conn.cursor()
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    return DataFrame(rows)


def isna(value):
    return value is None


__all__ = ["DataFrame", "Series", "ExcelWriter", "read_csv", "read_sql_query", "isna"]
