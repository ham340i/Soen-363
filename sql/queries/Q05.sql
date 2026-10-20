-- Individual ICU/CCU stays strictly longer than seven days.
SELECT p.given_name || ' ' || p.family_name AS patient_name,u.unit_type,s.entry_timestamp,s.exit_timestamp,
ROUND(julianday(s.exit_timestamp)-julianday(s.entry_timestamp),2) AS stay_days
FROM unit_stays s JOIN hospital_units u ON u.unit_id=s.unit_id
JOIN admissions a ON a.admission_id=s.admission_id JOIN patients p ON p.patient_id=a.patient_id
WHERE u.unit_type IN ('ICU','CCU') AND s.exit_timestamp IS NOT NULL
AND julianday(s.exit_timestamp)-julianday(s.entry_timestamp)>7
ORDER BY stay_days DESC;
