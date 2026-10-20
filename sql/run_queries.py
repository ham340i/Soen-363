"""Run Q01-Q20 against hospital.db; export reproducible CSV results."""
from pathlib import Path
import sqlite3,csv
root=Path(__file__).resolve().parents[1]
conn=sqlite3.connect(root/'hospital.db')
counts=[]
for file in sorted((root/'sql/queries').glob('Q*.sql')):
    cur=conn.execute(file.read_text())
    rows=cur.fetchall()
    with (root/'results'/(file.stem+'.csv')).open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow([c[0] for c in cur.description]);writer.writerows(rows)
    counts.append((file.stem,len(rows)))
    print(file.stem, len(rows))
(root/'results'/'QUERY_ROW_COUNTS.txt').write_text('\n'.join(f'{n}: {c} rows' for n,c in counts)+'\n')
conn.close()
