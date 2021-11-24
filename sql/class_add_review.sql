INSERT INTO review (review_id, content, date, uni, section, course_id)
VALUES(DEFAULT, :content, CURRENT_DATE, :uni, :section, :course_id);
