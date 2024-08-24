-- a SQL script that creates a view need_meeting that meets these requirements:
   -- view need_meeting should return all students name when:
   -- They score are under (strict) to 80
   -- AND no last_meeting date OR more than a month
   
CREATE VIEW need_meeting AS SELECT name from students WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < DATE(CURDATE() - INTERVAL 1 MONTH));
