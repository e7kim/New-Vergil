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

FROM instructor i, class cl, course cr, building b, department d, wishlist w
WHERE w.uni = :uni AND
      w.section = cl.section AND
      w.course_id = cl.course_id AND
      cl.uni = i.uni AND
      cl.building_code = b.building_code AND
      cr.department_code = d.department_code AND
      cl.course_id = cr.course_id
ORDER BY d.department_name, cr.course_id, cl.section
;
