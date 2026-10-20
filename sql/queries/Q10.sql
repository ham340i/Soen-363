
-- Patients who had surgery before entering ICU or CCU
-- during the same admission.

WITH critical_stays AS (
    SELECT
        s.admission_id,
        s.entry_timestamp,
        u.unit_type
    FROM unit_stays s
    JOIN hospital_units u
        ON u.unit_id = s.unit_id
    WHERE u.unit_type IN ('ICU', 'CCU')
),
surgery_admissions AS (
    SELECT
        sp.admission_id,
        sp.started_at,
        sp.ended_at,
        a.patient_id
    FROM surgical_procedures sp
    JOIN admissions a
        ON a.admission_id = sp.admission_id
)
SELECT
    p.given_name || ' ' || p.family_name AS patient_name,
    sa.started_at AS procedure_datetime,
    cs.unit_type,
    cs.entry_timestamp AS unit_entry_time
FROM surgery_admissions sa
JOIN patients p
    ON p.patient_id = sa.patient_id
JOIN critical_stays cs
    ON cs.admission_id = sa.admission_id
WHERE julianday(sa.ended_at) <
      julianday(cs.entry_timestamp)
ORDER BY
    p.patient_id ASC,
    sa.started_at ASC;
