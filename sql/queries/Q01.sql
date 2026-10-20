
-- Patients discharged without undergoing surgery.
SELECT
    p.given_name || ' ' || p.family_name AS patient_name,
    a.admission_timestamp,
    d.discharge_timestamp
FROM admissions a
JOIN patients p
    ON p.patient_id = a.patient_id
JOIN discharge_records d
    ON d.admission_id = a.admission_id
LEFT JOIN surgical_procedures s
    ON s.admission_id = a.admission_id
WHERE s.procedure_id IS NULL
ORDER BY a.admission_timestamp ASC;
