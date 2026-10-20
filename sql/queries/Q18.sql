-- Latest note per patient, window ranking handles multiple admissions and time ties deterministically.
WITH ranked AS (
 SELECT a.patient_id,n.note_type,n.note_timestamp,n.note_text,
 ROW_NUMBER() OVER(PARTITION BY a.patient_id ORDER BY julianday(n.note_timestamp) DESC,n.note_id DESC) AS rn
 FROM clinical_notes n JOIN admissions a ON a.admission_id=n.admission_id)
SELECT p.given_name || ' ' || p.family_name AS patient_name,r.note_type,r.note_timestamp,r.note_text
FROM ranked r JOIN patients p ON p.patient_id=r.patient_id WHERE r.rn=1 ORDER BY p.patient_id;
