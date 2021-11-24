-- Select all buildings where classes are taught

SELECT DISTINCT c.building_code, b.building_name
FROM class c, building b
WHERE c.building_code = b.building_code
ORDER BY b.building_name
;
