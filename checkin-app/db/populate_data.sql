INSERT INTO WEB_ACCOUNT (id, usrname, pswd) 
VALUES (1, 'teacher', 'teacher');

INSERT INTO STUDENT (id, student_id, student_fname, student_lname, fingerprint_id)
VALUES (1, '2052563', 'Kiet', 'Tran Quang', 1),
(2, '1852161', 'Go', 'Ho', 2);

INSERT INTO CHECKIN_STATUS (id, checkin_date, checkin_status, STUDENT_id)
VALUES (1, '2021-11-19', 'NONE', 1),
(2, '2021-11-19', 'NONE', 2);
