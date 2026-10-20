
-- High-priority emergency patients (triage priority levels 1 and 2).
SELECT DISTINCT
    p.patient_id,
    p.given_name || ' ' || p.family_name AS patient_name,
    a.admission_timestamp
FROM patients p
JOIN admissions a ON a.patient_id = p.patient_id
JOIN triage_assessments t ON t.admission_id = a.admission_id
WHERE a.admission_type = 'EMERGENCY'
  AND t.priority IN (1, 2)
ORDER BY a.admission_timestamp ASC;
