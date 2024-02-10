INSERT INTO poulaillers (poule_name, fermier_id, last_harvest, path, production)
SELECT poule_name, '549248069447843850', '2024-01-21 19:00:00', path, production
FROM poulaillers
WHERE fermier_id = 453869081662193686;
