
-- Patients who died during hospitalization,
-- including their primary ICD-9 diagnosis.

WITH deceased_admissions AS (
    SELECT
        a.admission_id,
        a.admission_timestamp,
        p.given_name,
        p.family_name,
        p.death_timestamp
    FROM admissions a
    JOIN patients p
        ON p.patient_id = a.patient_id
    JOIN discharge_records dr
        ON dr.admission_id = a.admission_id
    WHERE p.deceased = 'true'
      AND p.death_timestamp IS NOT NULL
      AND (
          INSTR(LOWER(dr.disposition), 'death') > 0
          OR INSTR(LOWER(dr.disposition), 'died') > 0
          OR INSTR(LOWER(dr.disposition), 'deceas') > 0
          OR INSTR(LOWER(dr.condition_at_discharge), 'deceas') > 0
          OR INSTR(LOWER(dr.condition_at_discharge), 'died') > 0
      )
),
primary_diagnoses AS (
    SELECT
        d.admission_id,
        d.icd9_code,
        i.official_title
    FROM diagnoses d
    JOIN icd9_dictionary i
        ON i.icd9_code = d.icd9_code
    WHERE d.diagnosis_role = 'PRIMARY'
)
SELECT
    da.given_name || ' ' || da.family_name AS patient_name,
    da.admission_timestamp,
    da.death_timestamp,
    pd.icd9_code,
    pd.official_title
FROM deceased_admissions da
JOIN primary_diagnoses pd
    ON pd.admission_id = da.admission_id
ORDER BY da.admission_timestamp ASC;
