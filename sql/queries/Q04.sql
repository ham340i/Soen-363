
-- Patients who had radiology and surgery
-- during the same hospital admission.

SELECT DISTINCT
    p.patient_id,
    p.given_name || ' ' || p.family_name AS patient_name,
    a.admission_id
FROM admissions a
JOIN patients p
    ON p.patient_id = a.patient_id
JOIN radiology_examinations r
    ON r.admission_id = a.admission_id
JOIN surgical_procedures s
    ON s.admission_id = a.admission_id
ORDER BY
    p.patient_id ASC,
    a.admission_id ASC;
