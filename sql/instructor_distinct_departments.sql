-- Select all departments where instructors are appointed

SELECT DISTINCT d.department_name, d.department_code
FROM instructor i, department d
WHERE i.department_code = d.department_code
ORDER BY d.department_name
;
