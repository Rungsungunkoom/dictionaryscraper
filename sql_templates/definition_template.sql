INSERT INTO definitions(definition, def_number, wordid)
VALUES ('{definition}', 1, (SELECT max(id) FROM words));