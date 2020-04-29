-- Insert a list of words in the word of the day worthy table, 
-- unless that word is already there.
INSERT INTO wotdworthy (wordid) 
SELECT ID as wordid 
FROM words 
WHERE Name in ({words}) AND 
wordid NOT in (SELECT wordid FROM wotdworthy);