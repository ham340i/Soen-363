#!/usr/bin/env python3
"""Check the supplied fictional CSV records. No database or SQL operations."""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


FILES = {
    "patients": "patient_id", "admissions": "admission_id",
    "triage_assessments": "triage_id", "healthcare_professionals": "professional_id",
    "hospital_units": "unit_id", "unit_stays": "stay_id",
    "diagnostic_orders": "order_id", "diagnostic_examinations": "examination_id",
    "radiology_examinations": "radiology_id", "radiology_reports": "report_id",
    "surgical_procedures": "procedure_id", "clinical_notes": "note_id",
    "diagnoses": "diagnosis_id", "icd9_dictionary": "icd9_code",
    "discharge_records": "discharge_id",
}
REFERENCES = {key: name for name, key in FILES.items()}
REFERENCES.update({key: "healthcare_professionals" for key in [
    "attending_professional_id", "ordering_professional_id", "performing_professional_id",
    "radiologist_id", "surgeon_id", "diagnosing_professional_id", "discharging_professional_id"]})
TIMES = {
    "patients": ["death_timestamp"], "admissions": ["admission_timestamp"],
    "triage_assessments": ["assessed_at"], "unit_stays": ["entry_timestamp", "exit_timestamp"],
    "diagnostic_orders": ["ordered_at"], "diagnostic_examinations": ["performed_at", "result_at"],
    "radiology_examinations": ["started_at", "ended_at"], "radiology_reports": ["reported_at"],
    "surgical_procedures": ["started_at", "ended_at"], "clinical_notes": ["note_timestamp"],
    "diagnoses": ["recorded_at"], "discharge_records": ["discharge_timestamp"],
}
REQUIRED = {
    "patients": ["date_of_birth", "deceased"],
    "admissions": ["patient_id", "status", "attending_professional_id"],
    "triage_assessments": ["admission_id", "professional_id", "priority"],
    "healthcare_professionals": ["role"], "hospital_units": ["unit_type"],
    "unit_stays": ["admission_id", "unit_id"],
    "diagnostic_orders": ["admission_id", "ordering_professional_id", "order_type"],
    "diagnostic_examinations": ["admission_id", "order_id", "professional_id", "examination_type"],
    "radiology_examinations": ["admission_id", "examination_id", "performing_professional_id"],
    "radiology_reports": ["radiology_id", "radiologist_id"],
    "surgical_procedures": ["admission_id", "surgeon_id"],
    "clinical_notes": ["admission_id", "professional_id", "note_type", "note_text"],
    "diagnoses": ["admission_id", "icd9_code", "diagnosis_role", "diagnosing_professional_id"],
    "icd9_dictionary": ["official_title", "description", "disease_category"],
    "discharge_records": ["admission_id", "disposition", "discharging_professional_id"],
}


def validate(root):
    errors, data, indexes, parsed = [], {}, {}, {}

    def check(ok, message):
        if not ok:
            errors.append(message)

    for name, key in FILES.items():
        try:
            with (root / f"{name}.csv").open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, strict=True)
                required = {key, *REQUIRED[name], *TIMES.get(name, [])}
                if not required.issubset(reader.fieldnames or []):
                    errors.append(f"{name}: missing columns {sorted(required - set(reader.fieldnames or []))}")
                    continue
                rows = list(reader)
                if any(None in r or any(v is None for v in r.values()) for r in rows):
                    errors.append(f"{name}: row width does not match header")
                    continue
                data[name] = rows
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f"{name}: cannot read CSV: {exc}")
            continue
        counts = Counter(r[key] for r in rows)
        check("" not in counts, f"{name}: blank ID")
        for value, count in counts.items():
            check(count == 1, f"{name}: duplicate ID {value}")
        indexes[name] = {r[key]: r for r in rows}
        for row in rows:
            label = f"{name}/{row[key]}"
            for col in TIMES.get(name, []):
                value = row[col]
                if not value and name == "patients":
                    continue
                try:
                    dt = datetime.fromisoformat(value)
                    if dt.tzinfo is None or dt.utcoffset() is None:
                        raise ValueError("timezone offset missing")
                    parsed[(name, row[key], col)] = dt
                except ValueError:
                    errors.append(f"{label}: invalid timestamp {col}={value!r}")
            for col in REQUIRED[name]:
                check(bool(row[col]), f"{label}: blank required value {col}")
    # Parsing failures prevent safe comparisons. Report them without crashing.
    if errors:
        return errors, data

    def dt(name, row, col):
        return parsed.get((name, row[FILES[name]], col))

    for name, rows in data.items():
        for row in rows:
            for col, value in row.items():
                if col in REFERENCES and col != FILES[name]:
                    check(value in indexes[REFERENCES[col]], f"{name}/{row[FILES[name]]}: missing reference {col}={value}")
    if errors:
        return errors, data

    discharges = defaultdict(list)
    primaries = Counter()
    stays = defaultdict(list)
    patient_admissions = defaultdict(list)
    for row in data["discharge_records"]:
        discharges[row["admission_id"]].append(row)
    for row in data["diagnoses"]:
        check(row["diagnosis_role"] in ("PRIMARY", "SECONDARY"), f"diagnoses/{row['diagnosis_id']}: invalid role")
        if row["diagnosis_role"] == "PRIMARY":
            primaries[row["admission_id"]] += 1
    bounds = {}
    for row in data["admissions"]:
        aid = row["admission_id"]
        start = dt("admissions", row, "admission_timestamp")
        records = discharges[aid]
        if row["status"] == "COMPLETED":
            check(len(records) == 1, f"{aid}: completed admission must have one generated discharge record")
            check(primaries[aid] >= 1, f"{aid}: completed admission without a primary diagnosis")
        if len(records) == 1:
            end = dt("discharge_records", records[0], "discharge_timestamp")
            check(start < end, f"{aid}: discharge before or equal to admission")
            bounds[aid] = (start, end)
            patient_admissions[row["patient_id"]].append((start, end, aid))

    for name, rows in data.items():
        for row in rows:
            aid = row.get("admission_id")
            if aid in bounds:
                start, end = bounds[aid]
                for col in TIMES.get(name, []):
                    value = dt(name, row, col)
                    check(start <= value <= end, f"{name}/{row[FILES[name]]}: {col} outside admission {aid}")
            for left, right in [("entry_timestamp", "exit_timestamp"), ("started_at", "ended_at"), ("performed_at", "result_at")]:
                if left in row and right in row:
                    check(dt(name, row, left) < dt(name, row, right), f"{name}/{row[FILES[name]]}: {right} before or equal to {left}")

    for row in data["unit_stays"]:
        stays[row["admission_id"]].append(row)
    for aid, rows in stays.items():
        rows.sort(key=lambda r: dt("unit_stays", r, "entry_timestamp"))
        for prev, current in zip(rows, rows[1:]):
            check(dt("unit_stays", prev, "exit_timestamp") <= dt("unit_stays", current, "entry_timestamp"), f"{aid}: overlapping unit stays")

    for row in data["diagnostic_examinations"]:
        order = indexes["diagnostic_orders"][row["order_id"]]
        check(row["admission_id"] == order["admission_id"], f"{row['examination_id']}: order belongs to another admission")
        check(row["examination_type"] == order["order_type"], f"{row['examination_id']}: order/examination type mismatch")
        check(dt("diagnostic_orders", order, "ordered_at") <= dt("diagnostic_examinations", row, "performed_at"), f"{row['examination_id']}: examination before order")
    for row in data["radiology_examinations"]:
        exam = indexes["diagnostic_examinations"][row["examination_id"]]
        check(row["admission_id"] == exam["admission_id"], f"{row['radiology_id']}: examination belongs to another admission")
        check(exam["examination_type"] == "RADIOLOGY", f"{row['radiology_id']}: linked examination is not radiology")
        check(dt("radiology_examinations", row, "started_at") == dt("diagnostic_examinations", exam, "performed_at"), f"{row['radiology_id']}: inconsistent examination time")
        check(dt("radiology_examinations", row, "ended_at") <= dt("diagnostic_examinations", exam, "result_at"), f"{row['radiology_id']}: result before examination ended")
    for row in data["radiology_reports"]:
        exam = indexes["radiology_examinations"][row["radiology_id"]]
        report_time = dt("radiology_reports", row, "reported_at")
        check(dt("radiology_examinations", exam, "ended_at") <= report_time, f"{row['report_id']}: report before imaging ended")
        if exam["admission_id"] in bounds:
            start, end = bounds[exam["admission_id"]]
            check(start <= report_time <= end, f"{row['report_id']}: report outside generated admission")

    for patient in data["patients"]:
        pid = patient["patient_id"]
        try:
            birth = date.fromisoformat(patient["date_of_birth"])
        except ValueError:
            errors.append(f"{pid}: invalid date_of_birth")
            continue
        check(patient["deceased"] in ("true", "false"), f"{pid}: invalid deceased flag")
        death = dt("patients", patient, "death_timestamp")
        check((patient["deceased"] == "true") == (death is not None), f"{pid}: death flag/timestamp mismatch")
        if death:
            check(birth <= death.date(), f"{pid}: death before birth")
        episodes = sorted(patient_admissions[pid])
        for start, end, aid in episodes:
            check(birth < start.date(), f"{pid}/{aid}: admission before birth")
            if death:
                check(start < death and end <= death, f"{pid}/{aid}: admission extends beyond death")
            if discharges[aid][0]["disposition"] == "DECEASED":
                check(death == end, f"{pid}/{aid}: deceased discharge does not match recorded death")
        for prev, current in zip(episodes, episodes[1:]):
            check(prev[1] <= current[0], f"{pid}: overlapping admissions {prev[2]} and {current[2]}")
    for row in data["triage_assessments"]:
        check(row["priority"] in ("1", "2", "3", "4", "5"), f"{row['triage_id']}: invalid synthetic triage priority")
    return errors, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    errors, data = validate(args.data_dir)
    for name in FILES:
        print(f"{name}.csv: {len(data.get(name, []))} records")
    if errors:
        print(f"FAIL: {len(errors)} data error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: 15 CSV datasets; 0 data errors.")
    print("Checked unique IDs, references, timestamps, admission bounds, primary diagnoses,")
    print("ICD-9 references, order/examination/report timing, transfers, birth/death consistency,")
    print("and non-overlapping patient admissions. Checks apply to these source files only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
