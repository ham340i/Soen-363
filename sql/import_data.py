"""Import the educational synthetic CSV dataset into SQLite (stdlib only)."""
from pathlib import Path
import sqlite3, csv
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'hospital.db'
order=['patients','healthcare_professionals','hospital_units','icd9_dictionary','admissions','triage_assessments','clinical_notes','diagnostic_orders','diagnostic_examinations','radiology_examinations','radiology_reports','surgical_procedures','unit_stays','diagnoses','discharge_records']
if DB.exists(): DB.unlink()
with sqlite3.connect(DB) as conn:
    conn.executescript((ROOT/'sql/schema.sql').read_text())
    for table in order:
        with (ROOT/'data'/f'{table}.csv').open(newline='',encoding='utf-8-sig') as fh:
            rows=list(csv.DictReader(fh))
        if not rows: continue
        cols=list(rows[0]); keys=', '.join('"'+x+'"' for x in cols)
        placeholders=', '.join('?' for _ in cols)
        conn.executemany(f'INSERT INTO {table} ({keys}) VALUES ({placeholders})', [[r[c] if r[c]!='' else None for c in cols] for r in rows])
        print(f'{table}: {len(rows)} rows')
    errors=conn.execute('PRAGMA foreign_key_check').fetchall()
    if errors: raise RuntimeError(f'Foreign key errors: {errors[:10]}')
print(f'Database created: {DB}')
