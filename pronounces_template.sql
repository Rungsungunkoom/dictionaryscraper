INSERT INTO pronounces(ipa, wordid)
VALUES ('{ipa}', (SELECT max(id) FROM words));