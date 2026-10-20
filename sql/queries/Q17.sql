-- Admissions with more than one distinct ICD-9 code.
SELECT p.given_name || ' ' || p.family_name AS patient_name,a.admission_id,
COUNT(DISTINCT d.icd9_code) AS distinct_icd9_codes
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
JOIN diagnoses d ON d.admission_id=a.admission_id
GROUP BY a.admission_id HAVING COUNT(DISTINCT d.icd9_code)>1 ORDER BY a.admission_id;
