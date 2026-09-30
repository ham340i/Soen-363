# Synthetic hospital data generation notes

## Fictional data

All patients, professionals, hospital units, encounters, findings, notes, and outcomes are invented for educational data testing. No patient records, real identities, contact details, health card numbers, or other personal information were used. Constructed names have explicit synthetic labels. ICD-9-CM codes and official titles are public reference terminology, not invented patient information.

These CSVs are adaptable source files. Their headers and linking labels describe this generated extract; they do not prescribe the team's database design.

## Generated datasets and record counts

Counts exclude CSV headers.

| File | Records |
| --- | ---: |
| patients.csv | 60 |
| admissions.csv | 120 |
| triage_assessments.csv | 120 |
| healthcare_professionals.csv | 25 |
| hospital_units.csv | 12 |
| unit_stays.csv | 349 |
| diagnostic_orders.csv | 340 |
| diagnostic_examinations.csv | 340 |
| radiology_examinations.csv | 100 |
| radiology_reports.csv | 100 |
| surgical_procedures.csv | 41 |
| clinical_notes.csv | 750 |
| diagnoses.csv | 410 |
| icd9_dictionary.csv | 40 |
| discharge_records.csv | 120 |

Supporting files: `generate_data.py` reproduces the fictional records using the included dictionary; `validate_data.py` checks the CSV data; `VALIDATION_RESULTS.txt` contains the validation output.

## Generation method

Python's standard library was used with random seed `3632026`. Twelve fictional episode templates supply related presenting complaints, diagnoses, imaging findings, procedures, and unit movements. Seeded variation supplies birth dates, simple observations, and two persistent background diagnoses per patient. These records are deliberately patterned and do not estimate real clinical distributions or outcomes.

Patients P001–P005 receive five admissions each, P006–P015 three each, P016–P040 two each, and P041–P055 one each. P056–P060 have no admissions. Repeat admissions are spaced 45 days apart. Admission events run from January 3 through July 16, 2025. Event times are generated as offsets from each admission, with the discharge after all examinations and procedures.

The dictionary contains 40 selected ICD-9-CM diagnosis codes with exact full titles from [CMS Version 32, effective October 1, 2014](https://www.cms.gov/medicare/coding-billing/icd-10-codes/icd-9-cm-diagnosis-procedure-codes-abbreviated-and-full-code-titles), using `CMS32_DESC_LONG_DX.txt` from the [CMS reference archive](https://www.cms.gov/medicare/coding/icd9providerdiagnosticcodes/downloads/icd-9-cm-v32-master-descriptions.zip). The archive's text was decoded as Windows-1252 and the selected titles written as UTF-8. Code punctuation was restored after the third digit. Dictionary descriptions are explanatory labels; disease categories are broad generation labels, not an official grouping system. Some reference codes intentionally have no corresponding diagnosis records.

The requested example `410.9` is represented by the more specific `410.91`, which identifies an initial episode of care. The included code title specifies that detail. `401.9`, `250.00`, and `272.4` are included directly. ICD-9-CM was chosen to match the requested educational terminology; this extract does not claim to reproduce current Canadian coding practice.

To regenerate and validate from the project folder:

```sh
python3 data/generate_data.py
python3 data/validate_data.py
```

Regeneration overwrites the 14 fictional record CSVs and retains `icd9_dictionary.csv` as the reference input. The generator and validator require no packages, database, or network access. The saved validation output applies to the delivered files; rerun the validator after modifying them. To refresh the saved output, redirect the validator's output to `data/VALIDATION_RESULTS.txt`.

## Deliberate edge cases

- High-priority emergency presentations, including priorities 1 and 2; less urgent examples use 3 and 4.
- Patients with more than three admissions, different primary diagnoses on separate admissions, and varying lengths of stay.
- Five patients with no admissions, plus admitted patients P054 and P055 with no radiology examinations in any admission.
- Completed admissions without surgery, and admissions containing both radiology and surgery.
- ICU and CCU stays individually longer than seven days. There are also CCU stays of exactly seven days and of six and a half days, to distinguish strict threshold boundaries.
- Direct ED-to-ICU and ED-to-CCU transfers.
- MICU, SICU, ICU, and CCU records; multiple unit transfers and more than one critical-care unit type within an admission.
- Surgery ending before subsequent ICU entry; complex surgical episodes pass through SICU and ICU.
- Radiology examinations in admissions without any ICU, CCU, MICU, or SICU stay.
- Radiology and surgery on the same calendar day, with imaging and its report preceding surgery.
- Distinct diagnoses within one admission, a primary plus secondary diagnoses, and reused ICD-9 codes across patients and admissions.
- Clinical assessment, progress, transfer, operative, and discharge-summary notes at different appropriate times.
- Discharge summaries using `recovery`, `Recovery`, `RECOVERY`, and `ReCoVeRy`. Deceased discharge summaries omit claims of recovery.
- Three deceased patients, each dying at the end of their final admission, and 57 non-deceased patients. No later admissions are generated for deceased patients.

## Import cleaning and transformation

- Files are UTF-8 CSVs with one header row. Use a CSV reader that handles quoted commas, including those in ICD titles and narrative text.
- Preserve all IDs and ICD-9 values as text. Spreadsheet number conversion can remove leading zeros from `038.9` or trailing zeros from `250.00`. Do not round, trim code digits, or convert codes to numbers.
- Dates use `YYYY-MM-DD`. Timestamps use ISO 8601 with an explicit UTC offset (`+00:00`). Keep that offset or convert consistently before comparisons. Same-calendar-day examples are defined using UTC.
- An empty death timestamp means no death recorded in this synthetic extract. Transform empty cells into your chosen missing-value representation when adapting the data.
- The deceased flag is the text `true` or `false`; triage priority and heart rate are integers, and temperature is a decimal in degrees Celsius. `recorded_sex` contains `F`, `M`, and `X`; `X` is a synthetic other/unspecified marker and is not an inference about gender identity.
- Preserve narrative capitalization if testing text searches. Categorical labels such as `PRIMARY`, `COMPLETED`, and `DISCHARGE_SUMMARY` are uppercase.
- Every radiology examination also appears in `diagnostic_examinations.csv`. Its `examination_id` points to that same event; the two files are not separate tests. The radiology file adds imaging details, and the report file supplies its fictional interpretation.
- Reference labels connect the source files. Any renaming, regrouping, or mapping should be chosen by the team when adapting these files to its independently created design.

## Assumptions strictly for generation

- This is one fictional hospital and an adult-only sample. All 120 admissions are emergency admissions and are completed; there are no ongoing episodes or pending/cancelled diagnostic orders in this extract.
- Priority 1 is the most urgent and priority 5 the least urgent on a simplified synthetic scale. It is not a validated clinical triage assignment.
- Each completed episode has one discharge record and one primary diagnosis, plus secondary diagnoses. These are generation choices for this sample, not requirements for the team's design.
- Deceased episodes still use admission status `COMPLETED`; the discharge disposition and patient death fields carry the outcome. Death and discharge timestamps coincide for these three episodes.
- Unit stays describe the responsible service during an admission. Brief trips to imaging or the operating room do not create additional unit stays. Operating room labels describe fictional locations rather than additional hospital-unit records. Consecutive unit stays meet at the transfer timestamp without overlapping.
- ICU, CCU, MICU, and SICU are distinct unit-type labels. CCU means coronary care. STEP means step-down care; the remaining abbreviated unit labels have their full names in `hospital_units.csv`.
- Orders precede examinations. All radiology reports and results occur before discharge. Discharge summaries are timestamped at discharge, including the end of deceased episodes. Boundaries at discharge and transfer are intentional.
- Staff are fictional role assignments, not a staffing roster. Shift schedules, bed capacities, medication courses, treatment guidelines, and detailed clinical coding rules are outside this data generation exercise. Clinical narratives and laboratory observations are simplified synthetic examples.
- The validator checks source-data consistency: IDs, referenced records, valid dates/times, event ordering, admission bounds, primary diagnoses, dictionary references, linked examination identity, non-overlapping stays/admissions, and birth/death consistency. It does not assess the team's design or establish clinical validity.
- The delivered data passed validation with zero errors. On temporary copies, the validator also detected 12 deliberate corruptions covering duplicate IDs, missing references, malformed timestamps, reversed discharge/stay timing, out-of-admission examinations/radiology/surgery, missing primary diagnoses, invalid ICD-9 references, cross-admission examination links, and premature radiology reports.
