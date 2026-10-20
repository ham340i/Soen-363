-- Has radiology but no ICU or CCU on any stay for this admission.
SELECT a.admission_id,p.given_name || ' ' || p.family_name AS patient_name
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
WHERE EXISTS(SELECT 1 FROM radiology_examinations r WHERE r.admission_id=a.admission_id)
AND NOT EXISTS(SELECT 1 FROM unit_stays s JOIN hospital_units u ON u.unit_id=s.unit_id
 WHERE s.admission_id=a.admission_id AND u.unit_type IN ('ICU','CCU'))
ORDER BY a.admission_id ASC;
