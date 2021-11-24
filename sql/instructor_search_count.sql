SELECT COUNT (DISTINCT i.uni)
FROM instructor i, class cl, department d, building b
WHERE i.uni = cl.uni AND
      i.department_code = d.department_code AND
      i.building_code = b.building_code AND
      (
          i.uni = :uni OR
          LOWER(CONCAT(i.first_name, ' ', i.last_name)) LIKE :name OR
          i.building_code = :building_code OR
          i.department_code = :department_code OR
          LOWER(cl.course_id) = LOWER(:course_id)
      )
;
