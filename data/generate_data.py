#!/usr/bin/env python3
"""Generate fictional source CSVs only; no database or SQL operations.

Run after icd9_dictionary.csv is present. Uses only Python's standard library.
"""
import csv
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RNG = random.Random(3632026)
DATA = {}


def add(dataset, **row):
    DATA.setdefault(dataset, []).append(row)
    return next(iter(row.values()))


def stamp(value):
    return value.isoformat(timespec="seconds")


def numbered(dataset, prefix, **fields):
    key = f"{prefix}{len(DATA.get(dataset, [])) + 1:04d}"
    id_field = {
        "triage_assessments": "triage_id", "unit_stays": "stay_id",
        "diagnostic_orders": "order_id", "diagnostic_examinations": "examination_id",
        "radiology_examinations": "radiology_id", "radiology_reports": "report_id",
        "surgical_procedures": "procedure_id", "clinical_notes": "note_id",
        "diagnoses": "diagnosis_id", "discharge_records": "discharge_id",
    }[dataset]
    add(dataset, **{id_field: key}, **fields)
    return key


def main():
    with (ROOT / "icd9_dictionary.csv").open(newline="", encoding="utf-8") as f:
        dictionary = {r["icd9_code"]: r for r in csv.DictReader(f)}

    # Names are constructed labels, with no real identities or contact details.
    first = ["Aven", "Neri", "Talin", "Mira", "Oren", "Lumi", "Sora", "Evin", "Runa", "Zeli"]
    last = ["Fablebrook", "Cloudmere", "Willowcrest", "Starfen", "Mossvale", "Dawnridge"]
    patients = {}
    for p in range(1, 61):
        pid = f"P{p:03d}"
        row = dict(patient_id=pid, given_name=first[(p-1) % 10],
                   family_name=f"{last[(p-1)//10]}-Synthetic",
                   date_of_birth=date(RNG.randint(1942, 1999), RNG.randint(1, 12), RNG.randint(1, 28)).isoformat(),
                   recorded_sex=["F", "M", "X"][(p-1) % 3],
                   deceased="false", death_timestamp="")
        add("patients", **row)
        patients[pid] = DATA["patients"][-1]

    types = ["ED", "ICU", "CCU", "MICU", "SICU", "MED", "SURG", "CARD", "ORTH", "NEUR", "STEP", "REHAB"]
    names = ["Emergency Department", "Intensive Care", "Coronary Care", "Medical Intensive Care",
             "Surgical Intensive Care", "General Medicine", "General Surgery", "Cardiology",
             "Orthopedics", "Neurology", "Step-down Care", "Rehabilitation"]
    units = {}
    for i, (kind, name) in enumerate(zip(types, names), 1):
        units[kind] = f"U{i:02d}"
        add("hospital_units", unit_id=units[kind], unit_name=f"Fable Hospital {name}", unit_type=kind)

    staff_groups = [("PHYSICIAN", "Emergency medicine"), ("PHYSICIAN", "Internal medicine"),
                    ("PHYSICIAN", "Critical care"), ("SURGEON", "General surgery"),
                    ("SURGEON", "Orthopedic surgery"), ("RADIOLOGIST", "Diagnostic radiology"),
                    ("NURSE", "Emergency nursing"), ("NURSE", "Inpatient nursing"),
                    ("TECHNOLOGIST", "Laboratory medicine"), ("TECHNOLOGIST", "Radiology")]
    staff = {}
    for i in range(25):
        role, specialty = staff_groups[i % 10]
        hid = f"H{i+1:03d}"
        staff.setdefault(specialty, []).append(hid)
        add("healthcare_professionals", professional_id=hid,
            display_name=f"{first[i % 10]} Fictionstaff-{i+1:02d}", role=role, specialty=specialty)

    # Templates are fictional episode narratives, not treatment recommendations.
    # path entries specify the start hour of each responsible-unit stay.
    profiles = [
        dict(code="486", reason="Fever and shortness of breath", priority=2, hours=84,
             path=[("ED", 0), ("MED", 6)], image=("XR", "Chest", "Patchy lower-lung opacity.")),
        dict(code="410.91", reason="Acute chest discomfort", priority=1, hours=264,
             path=[("ED", 0), ("CCU", 3), ("CARD", 207)], image=("XR", "Chest", "Mild pulmonary vascular congestion.")),
        dict(code="540.9", reason="Right lower abdominal pain", priority=2, hours=60,
             path=[("ED", 0), ("SURG", 4)], image=("CT", "Abdomen and pelvis", "Inflamed appendix without visible abscess."),
             surgery="Laparoscopic appendectomy"),
        dict(code="574.00", reason="Right upper abdominal pain", priority=3, hours=72,
             path=[("ED", 0), ("SURG", 4)], image=("US", "Upper abdomen", "Gallstones with gallbladder wall thickening."),
             surgery="Laparoscopic cholecystectomy"),
        dict(code="820.21", reason="Hip pain after a fictional fall", priority=2, hours=144,
             path=[("ED", 0), ("ORTH", 4), ("REHAB", 96)], image=("XR", "Hip", "Intertrochanteric fracture."),
             surgery="Internal fixation of hip fracture"),
        dict(code="038.9", reason="Fever with circulatory instability", priority=1, hours=336,
             path=[("ED", 0), ("MICU", 3), ("ICU", 51), ("STEP", 255)],
             image=("XR", "Chest", "Bilateral patchy pulmonary opacities."), secondary=["995.92", "785.52", "486"]),
        dict(code="518.81", reason="Severe breathing difficulty", priority=1, hours=288,
             path=[("ED", 0), ("ICU", 2), ("MICU", 206), ("MED", 254)],
             image=("XR", "Chest", "Diffuse bilateral airspace opacities."), secondary=["486"]),
        dict(code="276.51", reason="Dizziness with reduced fluid intake", priority=3, hours=24,
             path=[("ED", 0), ("MED", 5)], image=None),
        dict(code="434.91", reason="Sudden limb weakness", priority=2, hours=120,
             path=[("ED", 0), ("NEUR", 5), ("REHAB", 84)],
             image=("CT", "Head", "Focal ischemic change without visible hemorrhage.")),
        dict(code="682.6", reason="Lower-leg redness and swelling", priority=4, hours=36,
             path=[("ED", 0), ("MED", 6)], image=None),
        dict(code="562.11", reason="Severe abdominal pain with systemic illness", priority=2, hours=300,
             path=[("ED", 0), ("SURG", 4), ("SICU", 9), ("ICU", 57), ("STEP", 249), ("SURG", 273)],
             image=("CT", "Abdomen and pelvis", "Inflamed colonic diverticula with surrounding inflammatory change."),
             surgery="Segmental colectomy", secondary=["518.81"]),
        dict(code="428.0", reason="Breathlessness with leg swelling", priority=2, hours=96,
             path=[("ED", 0), ("CARD", 5)], image=("XR", "Chest", "Pulmonary edema and enlarged cardiac silhouette.")),
    ]
    chronic = ["401.9", "250.00", "272.4", "244.9", "530.81", "285.9"]
    chronic_by_patient = {p: RNG.sample(chronic, 2) for p in patients}
    aid_num = 0
    for p in range(1, 56):
        visits = 5 if p <= 5 else 3 if p <= 15 else 2 if p <= 40 else 1
        pid = f"P{p:03d}"
        for v in range(visits):
            aid_num += 1
            aid = f"A{aid_num:04d}"
            profile = profiles[(p - 1 + v * 3) % len(profiles)]
            died = p in (12, 33, 49) and v == visits - 1
            if died:
                profile = profiles[5 if p != 33 else 6]
            if p in (54, 55):
                profile = profiles[7 if p == 54 else 9]
            # Boundary examples around a seven-day CCU stay.
            if p in (2, 14) and v == 0:
                profile = dict(profile, path=[("ED", 0), ("CCU", 3),
                                             ("CARD", 171 if p == 2 else 159)])
            start = datetime(2025, 1, 1, 7, tzinfo=timezone.utc) + timedelta(days=2*p + 45*v)
            duration = profile["hours"] + ((p + v) % 3) * 6
            end = start + timedelta(hours=duration)
            when = lambda h: stamp(start + timedelta(hours=h))
            physician = staff["Critical care" if profile["priority"] == 1 else "Internal medicine"][p % 3]
            emergency = staff["Emergency medicine"][p % 3]
            add("admissions", admission_id=aid, patient_id=pid, admission_timestamp=stamp(start),
                admission_type="EMERGENCY", status="COMPLETED", presenting_complaint=profile["reason"],
                attending_professional_id=physician)
            numbered("triage_assessments", "T", admission_id=aid, assessed_at=when(0.05),
                     professional_id=staff["Emergency nursing"][p % 2], priority=profile["priority"],
                     chief_complaint=profile["reason"],
                     heart_rate_bpm=RNG.randint(102, 128) if profile["priority"] == 1 else RNG.randint(74, 105),
                     temperature_c=round(RNG.uniform(38.0, 39.1) if profile["code"] in ("486", "038.9", "682.6") else RNG.uniform(36.5, 37.6), 1))

            for ix, (kind, hour) in enumerate(profile["path"]):
                exit_hour = profile["path"][ix+1][1] if ix+1 < len(profile["path"]) else duration
                numbered("unit_stays", "ST", admission_id=aid, unit_id=units[kind],
                         entry_timestamp=when(hour), exit_timestamp=when(exit_hour))

            for label, ordered, performed, performer, result in [
                ("Complete blood count", .5, 1, staff["Laboratory medicine"][p % 2],
                 f"Synthetic WBC {RNG.uniform(10, 17):.1f} x10^9/L; review in episode context."),
                ("Basic metabolic panel", .75, 1.5, staff["Laboratory medicine"][(p+1) % 2],
                 f"Synthetic sodium {RNG.randint(135, 143)} mmol/L; other values omitted."),
            ]:
                oid = numbered("diagnostic_orders", "O", admission_id=aid, ordered_at=when(ordered),
                               ordering_professional_id=emergency, order_type="LABORATORY", requested_test=label, status="COMPLETED")
                numbered("diagnostic_examinations", "EX", admission_id=aid, order_id=oid,
                         performed_at=when(performed), result_at=when(performed+.25), professional_id=performer,
                         examination_type="LABORATORY", examination_name=label, result_text=result)

            if profile["image"]:
                modality, body, finding = profile["image"]
                oid = numbered("diagnostic_orders", "O", admission_id=aid, ordered_at=when(.6),
                               ordering_professional_id=emergency, order_type="RADIOLOGY",
                               requested_test=f"{modality} {body}", status="COMPLETED")
                exid = numbered("diagnostic_examinations", "EX", admission_id=aid, order_id=oid,
                               performed_at=when(2), result_at=when(2.75), professional_id=staff["Radiology"][p % 2],
                               examination_type="RADIOLOGY", examination_name=f"{modality} {body}",
                               result_text=f"Synthetic imaging: {finding}")
                rid = numbered("radiology_examinations", "R", admission_id=aid, examination_id=exid,
                               modality=modality, body_region=body, started_at=when(2), ended_at=when(2.3),
                               performing_professional_id=staff["Radiology"][p % 2])
                numbered("radiology_reports", "RP", radiology_id=rid, reported_at=when(2.75),
                         radiologist_id=staff["Diagnostic radiology"][p % 2],
                         findings=f"Fictional examination. {finding}", impression=finding, report_status="FINAL")

            if "surgery" in profile:
                specialty = "Orthopedic surgery" if profile["code"] == "820.21" else "General surgery"
                numbered("surgical_procedures", "S", admission_id=aid, procedure_name=profile["surgery"],
                         surgeon_id=staff[specialty][p % 3], started_at=when(6), ended_at=when(8),
                         location_label="Fictional operating room 01", procedure_status="COMPLETED")

            entries = [("CLINICAL_ASSESSMENT", .3, emergency,
                        f"Fictional assessment: {profile['reason']}. Examination documented; diagnostic evaluation requested."),
                       ("PROGRESS", 4, physician,
                        "Synthetic results reviewed; monitoring continues during this admission."),
                       ("PROGRESS", duration/2, physician,
                        "Synthetic interval review: ongoing inpatient observation and reassessment.")]
            if "surgery" in profile:
                entries.append(("OPERATIVE", 8.2, staff[specialty][p % 3],
                                f"Fictional procedure completed: {profile['surgery']}. Postoperative monitoring arranged."))
            for ix, (kind, hour) in enumerate(profile["path"][1:], 1):
                entries.append(("TRANSFER", hour, physician,
                                f"Fictional transfer from {profile['path'][ix-1][0]} to {kind}; responsible unit changed."))
            word = ["recovery", "Recovery", "RECOVERY", "ReCoVeRy"][aid_num % 4]
            summary = ("Fictional episode ended with in-hospital death; family discussion documented."
                       if died else f"Fictional discharge summary: {word} documented; follow-up arranged.")
            entries.append(("DISCHARGE_SUMMARY", duration, physician, summary))
            for kind, hour, author, narrative in sorted(entries, key=lambda x: x[1]):
                numbered("clinical_notes", "N", admission_id=aid, professional_id=author,
                         note_timestamp=when(hour), note_type=kind, note_text=narrative)

            codes = list(dict.fromkeys([profile["code"]] + profile.get("secondary", []) + chronic_by_patient[pid]))
            for ix, code in enumerate(codes):
                assert code in dictionary, code
                numbered("diagnoses", "D", admission_id=aid, icd9_code=code,
                         diagnosis_role="PRIMARY" if ix == 0 else "SECONDARY",
                         recorded_at=when(duration-1), diagnosing_professional_id=physician)

            disposition = "DECEASED" if died else "REHABILITATION" if profile["path"][-1][0] == "REHAB" else "HOME"
            numbered("discharge_records", "DC", admission_id=aid, discharge_timestamp=stamp(end),
                     disposition=disposition, discharging_professional_id=physician,
                     condition_at_discharge="DECEASED" if died else "IMPROVED")
            if died:
                patients[pid].update(deceased="true", death_timestamp=stamp(end))

    for name, rows in DATA.items():
        with (ROOT / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"{name}.csv: {len(rows)}")
    print(f"icd9_dictionary.csv: {len(dictionary)}")


if __name__ == "__main__":
    main()
