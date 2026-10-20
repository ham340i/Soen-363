
-- Patients transferred from the Emergency Department
-- to ICU or CCU during the same admission.

WITH critical_care AS (
    SELECT
        s.admission_id,
        s.entry_timestamp
    FROM unit_stays s
    JOIN hospital_units u
        ON u.unit_id = s.unit_id
    WHERE u.unit_type IN ('ICU', 'CCU')
),
emergency_stays AS (
    SELECT
        s.admission_id,
        s.entry_timestamp
    FROM unit_stays s
    JOIN hospital_units u
        ON u.unit_id = s.unit_id
    WHERE u.unit_type = 'ED'
)
SELECT DISTINCT
    p.patient_id,
    p.given_name || ' ' || p.family_name AS patient_name,
    a.admission_id
FROM admissions a
JOIN patients p
    ON p.patient_id = a.patient_id
JOIN emergency_stays ed
    ON ed.admission_id = a.admission_id
JOIN critical_care cc
    ON cc.admission_id = a.admission_id
WHERE julianday(cc.entry_timestamp) >
      julianday(ed.entry_timestamp)
ORDER BY a.admission_id ASC;
