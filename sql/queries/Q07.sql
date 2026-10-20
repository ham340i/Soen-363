-- Identify an ED stay followed by a later ICU/CCU unit entry in the same admission.
SELECT DISTINCT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name,a.admission_id
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
JOIN unit_stays ed ON ed.admission_id=a.admission_id
JOIN hospital_units ued ON ued.unit_id=ed.unit_id
JOIN unit_stays cc ON cc.admission_id=a.admission_id
JOIN hospital_units ucc ON ucc.unit_id=cc.unit_id
WHERE ued.unit_type='ED' AND ucc.unit_type IN ('ICU','CCU')
AND julianday(cc.entry_timestamp)>julianday(ed.entry_timestamp)
ORDER BY a.admission_id ASC;
