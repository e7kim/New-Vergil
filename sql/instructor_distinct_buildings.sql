-- Select all buildings where instructors have offices

SELECT DISTINCT i.building_code, b.building_name
FROM instructor i, building b
WHERE i.building_code = b.building_code
ORDER BY b.building_name
;
