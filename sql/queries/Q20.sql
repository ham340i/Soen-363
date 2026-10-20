-- Surgery and radiology on the same calendar day and same admission.
SELECT DISTINCT p.given_name || ' ' || p.family_name AS patient_name,a.admission_id,
s.procedure_name AS procedure_type,r.modality AS radiology_type,date(s.started_at) AS common_date
FROM surgical_procedures s JOIN admissions a ON a.admission_id=s.admission_id
JOIN patients p ON p.patient_id=a.patient_id
JOIN radiology_examinations r ON r.admission_id=a.admission_id
WHERE date(s.started_at)=date(r.started_at)
ORDER BY a.admission_id ASC, common_date ASC;
