
"""Run the 20 approved hospital queries and export their results."""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY_DIR = ROOT / "sql" / "queries"
RESULTS_DIR = ROOT / "results"

# Only execute the 20 expected query files.
QUERY_NAMES = [f"Q{i:02d}" for i in range(1, 21)]


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    counts = []

    with sqlite3.connect(ROOT / "hospital.db") as connection:
        connection.execute("PRAGMA query_only = ON")

        for name in QUERY_NAMES:
            query_file = QUERY_DIR / f"{name}.sql"

            if not query_file.is_file():
                raise FileNotFoundError(f"Missing query: {query_file}")

            sql = query_file.read_text(encoding="utf-8").strip()

            if not sql.upper().startswith(("SELECT ", "WITH ")):
                raise ValueError(f"{name} must be a read-only query")

            cursor = connection.execute(sql)
            rows = cursor.fetchall()

            output_file = RESULTS_DIR / f"{name}.csv"

            with output_file.open(
                "w", encoding="utf-8", newline=""
            ) as output:
                writer = csv.writer(output)
                writer.writerow(
                    [column[0] for column in cursor.description]
                )
                writer.writerows(rows)

            counts.append((name, len(rows)))
            print(f"{name}: {len(rows)} rows")

    summary = "\n".join(
        f"{name}: {count} rows" for name, count in counts
    )

    (RESULTS_DIR / "QUERY_ROW_COUNTS.txt").write_text(
        summary + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
