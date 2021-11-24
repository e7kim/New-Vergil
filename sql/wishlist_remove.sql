DELETE FROM wishlist w
WHERE w.uni = :uni AND
      w.course_id = :course_id AND
      w.section = :section
;
