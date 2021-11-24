SELECT
    cl.section,
    cl.begin_time,
    cl.end_time,
    cl.enrollments,
    cl.days,

    cl.room_number,
    b.building_name,

    cr.course_id,
    cr.name,
    cr.points,

    d.department_name,

    i.uni,
    i.first_name,
    i.last_name

FROM instructor i, class cl, course cr, building b, department d
WHERE cl.uni = i.uni AND
      cl.building_code = b.building_code AND
      cr.department_code = d.department_code AND
      cl.course_id = cr.course_id AND
      (
          (i.uni = :uni OR :uni IS NULL) AND
          (cl.building_code = :building_code OR :building_code IS NULL) AND
          (cr.department_code = :department_code OR :department_code IS NULL) AND
          (LOWER(cl.course_id) = LOWER(:course_id) OR :course_id IS NULL) AND
          (LOWER(cr.name) LIKE :name OR :name IS NULL) AND
          (cl.days LIKE :days OR :days IS NULL) AND
          ((cl.begin_time >= :begin_time AND cl.begin_time < (:begin_time + INTERVAL '1 hour')) OR :begin_time IS NULL)
      )
ORDER BY d.department_name, cr.course_id, cl.section
LIMIT 3 OFFSET :offset
;
