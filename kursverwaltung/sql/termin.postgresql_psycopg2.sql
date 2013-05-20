-- Checkt Termine, ob sie beginnen *bevor* sie angefangen haben.
ALTER TABLE termin ADD CONSTRAINT termin_beginn_vor_ende CHECK (beginn < ende);
