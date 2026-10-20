
-- Admissions with radiology examinations
-- but without any ICU or CCU stay.

WITH radiology_admissions AS (
    SELECT DISTINCT admission_id
    FROM radiology_examinations
),
critical_admissions AS (
    SELECT DISTINCT s.admission_id
    FROM unit_stays s
    JOIN hospital_units u
        ON u.unit_id = s.unit_id
    WHERE u.unit_type IN ('ICU', 'CCU')
)
SELECT
    a.admission_id,
    p.given_name || ' ' || p.family_name AS patient_name
FROM admissions a
JOIN patients p
    ON p.patient_id = a.patient_id
JOIN radiology_admissions r
    ON r.admission_id = a.admission_id
LEFT JOIN critical_admissions c
    ON c.admission_id = a.admission_id
WHERE c.admission_id IS NULL
ORDER BY a.admission_id ASC;
