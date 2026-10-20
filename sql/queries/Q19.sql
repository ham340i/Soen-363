-- Deceased discharge and primary ICD-9 diagnosis.
SELECT p.given_name || ' ' || p.family_name AS patient_name,a.admission_timestamp,
p.death_timestamp,d.icd9_code,i.official_title
FROM admissions a JOIN patients p ON p.patient_id=a.patient_id
JOIN discharge_records dr ON dr.admission_id=a.admission_id
JOIN diagnoses d ON d.admission_id=a.admission_id AND d.diagnosis_role='PRIMARY'
JOIN icd9_dictionary i ON i.icd9_code=d.icd9_code
WHERE p.deceased='true' AND p.death_timestamp IS NOT NULL
AND (LOWER(dr.disposition) LIKE '%death%' OR LOWER(dr.disposition) LIKE '%died%' OR LOWER(dr.disposition) LIKE '%deceas%' OR LOWER(dr.condition_at_discharge) LIKE '%deceas%' OR LOWER(dr.condition_at_discharge) LIKE '%died%')
ORDER BY a.admission_timestamp;
