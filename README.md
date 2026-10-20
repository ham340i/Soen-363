# SOEN 363 — Hospital Management System (Phase 1)

This repository contains **entirely fictional, synthetic hospital data** for Concordia University's SOEN 363 Phase 1 project. It is intended for educational database development and testing. No real patient records or personally identifiable information were used.

> **Current scope:** This repository contains the data-source component and its validation tools. The CSV files are not themselves a relational database implementation.

## Repository structure

```text
Soen-363/
├── README.md
└── data/
    ├── *.csv                     # 15 datasets
    ├── generate_data.py          # Reproducible synthetic data generator
    ├── validate_data.py          # Source-data integrity checks
    ├── DATA_GENERATION_NOTES.md  # Sources, methodology, assumptions
    └── VALIDATION_RESULTS.txt    # Saved validation output
```

## Included datasets

| CSV file | Records |
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

See [Data Generation Notes](data/DATA_GENERATION_NOTES.md) for the data sources, generation approach, assumptions, and supported test scenarios.

## Requirements

- Python 3 (standard library only)
- No additional Python packages, database server, or network connection required to regenerate and validate the CSV data

## How to use

From the repository root, **validate the existing CSV files**:

```bash
python3 data/validate_data.py
```

To **regenerate the synthetic records and validate them**:

```bash
python3 data/generate_data.py
python3 data/validate_data.py
```

On Windows, try `py` instead of `python3` if needed. **Warning:** Regeneration overwrites 14 generated CSV files, retaining `icd9_dictionary.csv` as reference input.

The committed [validation results](data/VALIDATION_RESULTS.txt) report **PASS: 15 CSV datasets; 0 data errors**. Checks include unique identifiers, references between source files, time ordering, admission boundaries, diagnosis references, and related consistency checks. These checks do **not** establish that the finished SQL database meets all project requirements.

## Data handling notes

- CSV files are UTF-8 with headers. Use an importer that handles quoted commas.
- Preserve IDs and ICD-9 codes as **text** (for example, `038.9` and `250.00`).
- Timestamps use ISO 8601 and include a UTC offset (`+00:00`).
- Decide how empty values map to SQL `NULL` during import.
- The team must design the schema, table relationships, types, and constraints independently.

## Sources and academic integrity

All hospital records, patients, and professionals are synthetic. The ICD-9-CM code titles are based on the [Centers for Medicare & Medicaid Services (CMS) ICD-9-CM reference](https://www.cms.gov/medicare/coding-billing/icd-10-codes/icd-9-cm-diagnosis-procedure-codes-abbreviated-and-full-code-titles). The generator uses a fixed random seed, `3632026`, for reproducibility. For the full generation methodology, see [DATA_GENERATION_NOTES.md](data/DATA_GENERATION_NOTES.md).

The SOEN 363 Phase 1 handout permits generative AI for **Data Sources only**. The ER diagram, relational database implementation, SQL queries, and final submission must be completed by the project team in accordance with the course policy.

## Project status

The current repository includes synthetic hospital CSV datasets, generator/validator scripts, and data-source documentation. It does **not yet include** the ER diagram, SQL database schema/import scripts, 20 required SQL queries and their outputs, or the final PDF report.
