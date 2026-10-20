-- LEFT JOIN includes patients with no admissions and displays zero.
SELECT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name,COUNT(a.admission_id) AS total_admissions
FROM patients p LEFT JOIN admissions a ON a.patient_id=p.patient_id
GROUP BY p.patient_id ORDER BY p.patient_id;
