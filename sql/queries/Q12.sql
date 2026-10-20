-- Case-insensitive recovery keyword in discharge-summary notes.
SELECT DISTINCT p.patient_id,p.given_name || ' ' || p.family_name AS patient_name
FROM patients p JOIN admissions a ON a.patient_id=p.patient_id
JOIN clinical_notes n ON n.admission_id=a.admission_id
WHERE n.note_type='DISCHARGE_SUMMARY' AND LOWER(n.note_text) LIKE '%recovery%'
ORDER BY p.patient_id;
