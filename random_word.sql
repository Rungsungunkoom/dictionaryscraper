
SELECT '{' || '"title": "' || w.name || '", ' || '"url": "' || w.url || '", ' || '"description": ' || '"*' || c.class || '*. \r\n1. ' || d.definition || '"}' 
FROM words as w
JOIN classes as c on w.id = c.wordid
JOIN definitions as d on w.id = d.wordid
JOIN pronounces as p on w.id = p.wordid
WHERE d.def_number = 1
ORDER BY RANDOM() LIMIT 1