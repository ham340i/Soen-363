-- Surgery must be completed before the ICU/CCU stay begins.
SELECT p.given_name || ' ' || p.family_name AS patient_name,s.started_at AS procedure_datetime,
u.unit_type,st.entry_timestamp AS unit_entry_time
FROM surgical_procedures s JOIN admissions a ON a.admission_id=s.admission_id
JOIN patients p ON p.patient_id=a.patient_id JOIN unit_stays st ON st.admission_id=a.admission_id
JOIN hospital_units u ON u.unit_id=st.unit_id
WHERE u.unit_type IN ('ICU','CCU') AND julianday(s.ended_at)<julianday(st.entry_timestamp)
ORDER BY p.patient_id ASC, s.started_at ASC;
