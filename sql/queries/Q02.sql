-- Count hospital visits, keeping only patients with more than three admissions.
SELECT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name, COUNT(*) AS total_admissions
FROM patients p JOIN admissions a ON a.patient_id=p.patient_id
GROUP BY p.patient_id HAVING COUNT(*)>3 ORDER BY total_admissions DESC,p.patient_id;
