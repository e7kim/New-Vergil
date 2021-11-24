SELECT
    r.content,
    r.date,
    r.course_id,
    cr.name as course_name,
    r.section,
    i.first_name,
    i.last_name
FROM review r, instructor i, class cl, course cr
WHERE (r.course_id, r.section) = (cl.course_id, cl.section) AND
       r.course_id = cr.course_id AND
       cl.uni = i.uni AND
       (r.course_id, r.section) = (:course_id, :section)
;
