-- Completed admissions with a discharge record but no associated surgery.
SELECT p.given_name || ' ' || p.family_name AS patient_name,a.admission_timestamp,d.discharge_timestamp
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
JOIN discharge_records d ON d.admission_id=a.admission_id
WHERE NOT EXISTS(SELECT 1 FROM surgical_procedures s WHERE s.admission_id=a.admission_id)
ORDER BY a.admission_timestamp;
