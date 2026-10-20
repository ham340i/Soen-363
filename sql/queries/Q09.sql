-- Average completed unit stay duration by critical-care type.
SELECT u.unit_type,ROUND(AVG(julianday(s.exit_timestamp)-julianday(s.entry_timestamp)),2) AS avg_stay_days
FROM unit_stays s JOIN hospital_units u ON u.unit_id=s.unit_id
WHERE u.unit_type IN ('MICU','SICU','ICU','CCU') AND s.exit_timestamp IS NOT NULL
GROUP BY u.unit_type ORDER BY u.unit_type;
