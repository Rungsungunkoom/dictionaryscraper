INSERT INTO classes(class, wordid)
VALUES ('{class}', (SELECT max(id) FROM words));