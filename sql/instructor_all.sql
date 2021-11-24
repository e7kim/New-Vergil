SELECT DISTINCT
    i.first_name,
    i.last_name,
    i.uni,
    i.title,
    d.department_name,
    i.email,
    i.phone_number,
    b.building_name,
    i.room_number
FROM instructor i, class cl, department d, building b
WHERE i.uni = cl.uni AND
      i.department_code = d.department_code AND
      i.building_code = b.building_code
ORDER BY i.first_name, i.last_name
LIMIT 3 OFFSET :offset
;
