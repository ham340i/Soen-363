-- Per admission, first stay is not a transfer; sum subsequent stays by patient.
WITH per_admission AS (
 SELECT a.patient_id,a.admission_id,CASE WHEN COUNT(s.stay_id)>0 THEN COUNT(s.stay_id)-1 ELSE 0 END AS transfers
 FROM admissions a LEFT JOIN unit_stays s ON s.admission_id=a.admission_id
 GROUP BY a.admission_id)
SELECT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name,COALESCE(SUM(x.transfers),0) AS total_transfers
FROM patients p LEFT JOIN per_admission x ON x.patient_id=p.patient_id
GROUP BY p.patient_id
ORDER BY p.patient_id ASC;
