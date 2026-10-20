-- Use EXISTS to avoid duplicates when several exams or surgeries occur.
SELECT DISTINCT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name,a.admission_id
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
WHERE EXISTS(SELECT 1 FROM radiology_examinations r WHERE r.admission_id=a.admission_id)
AND EXISTS(SELECT 1 FROM surgical_procedures s WHERE s.admission_id=a.admission_id)
ORDER BY p.patient_id ASC, a.admission_id ASC;
