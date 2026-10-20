-- Include patients without radiology exams, avoid duplication over admissions.
SELECT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name,COUNT(r.radiology_id) AS radiology_count
FROM patients p LEFT JOIN admissions a ON a.patient_id=p.patient_id
LEFT JOIN radiology_examinations r ON r.admission_id=a.admission_id
GROUP BY p.patient_id
ORDER BY p.patient_id ASC;
