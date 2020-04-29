SELECT wotd.wordid as wordid
FROM wotdworthy as wotd
JOIN words as w on wotd.wordid = w.id
WHERE w.id NOT IN 
(SELECT wordid FROM wotdlogs WHERE guild = ?)
ORDER BY RANDOM() LIMIT 1