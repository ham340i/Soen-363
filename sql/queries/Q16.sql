-- More than one distinct critical-care unit type in the same admission.
SELECT p.given_name || ' ' || p.family_name AS patient_name,a.admission_id,
COUNT(DISTINCT u.unit_type) AS distinct_critical_types
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
JOIN unit_stays s ON s.admission_id=a.admission_id JOIN hospital_units u ON u.unit_id=s.unit_id
WHERE u.unit_type IN ('MICU','SICU','ICU','CCU')
GROUP BY a.admission_id
HAVING COUNT(DISTINCT u.unit_type) > 1
ORDER BY a.admission_id ASC;
