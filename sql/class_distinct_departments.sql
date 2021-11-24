-- Select all departments where classes are offered

SELECT DISTINCT d.department_name, d.department_code
FROM  course c, department d
WHERE c.department_code = d.department_code
ORDER BY d.department_name
;
