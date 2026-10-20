-- Maximum completed admission length, retaining all equal-length ties.
WITH lengths AS (SELECT a.admission_id,a.patient_id,a.admission_timestamp,d.discharge_timestamp,
ROUND((julianday(d.discharge_timestamp)-julianday(a.admission_timestamp))*24,2) AS stay_hours
FROM admissions a JOIN discharge_records d ON d.admission_id=a.admission_id)
SELECT p.given_name || ' ' || p.family_name AS patient_name,l.admission_id,l.admission_timestamp,l.discharge_timestamp,l.stay_hours
FROM lengths l JOIN patients p ON p.patient_id=l.patient_id
WHERE l.stay_hours=(SELECT MAX(stay_hours) FROM lengths)
ORDER BY p.patient_id ASC;
