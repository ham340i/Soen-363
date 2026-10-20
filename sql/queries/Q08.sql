-- Most common primary diagnosis in admissions involving ICU or CCU; show all ties.
WITH counts AS (
 SELECT d.icd9_code,i.official_title,COUNT(*) AS times_assigned
 FROM diagnoses d JOIN icd9_dictionary i ON i.icd9_code=d.icd9_code
 WHERE d.diagnosis_role='PRIMARY' AND EXISTS(
  SELECT 1 FROM unit_stays s JOIN hospital_units u ON u.unit_id=s.unit_id
  WHERE s.admission_id=d.admission_id AND u.unit_type IN ('ICU','CCU'))
 GROUP BY d.icd9_code,i.official_title)
SELECT icd9_code,official_title,times_assigned FROM counts
WHERE times_assigned=(SELECT MAX(times_assigned) FROM counts);
