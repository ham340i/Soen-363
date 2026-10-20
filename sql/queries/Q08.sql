
-- Most frequent primary ICD-9 diagnosis
-- among ICU or CCU admissions, including ties.

WITH critical_admissions AS (
    SELECT DISTINCT s.admission_id
    FROM unit_stays s
    JOIN hospital_units u
        ON u.unit_id = s.unit_id
    WHERE u.unit_type IN ('ICU', 'CCU')
),
counts AS (
    SELECT
        d.icd9_code,
        i.official_title,
        COUNT(*) AS times_assigned
    FROM diagnoses d
    JOIN icd9_dictionary i
        ON i.icd9_code = d.icd9_code
    JOIN critical_admissions ca
        ON ca.admission_id = d.admission_id
    WHERE d.diagnosis_role = 'PRIMARY'
    GROUP BY d.icd9_code, i.official_title
)
SELECT
    icd9_code,
    official_title,
    times_assigned
FROM counts
WHERE times_assigned = (
    SELECT MAX(times_assigned)
    FROM counts
);
