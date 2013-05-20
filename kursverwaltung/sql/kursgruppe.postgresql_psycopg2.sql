-- Überprüft ob die Teilnehmeranzahl kleiner gleich der maximalen Teilnehmerzahl des Kurses ist.
CREATE OR REPLACE FUNCTION num_tn_le_max_tn() RETURNS TRIGGER AS $$
DECLARE
    n INTEGER;
    k RECORD;
BEGIN
    SELECT COUNT(*) INTO n FROM student_belegt_kurs WHERE (kursgruppe_id = NEW.kursgruppe_id);
    SELECT * INTO k FROM kursgruppe WHERE (id = NEW.kursgruppe_id);
    IF n >= k.max_tn THEN
        RAISE EXCEPTION 'Zu viele Teilnehmer in %.', k.thema;
    ELSE
        RETURN NEW;
    END IF;
END; $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS num_tn_le_max_tn_trigger ON student_belegt_kurs;
CREATE TRIGGER num_tn_le_max_tn_trigger BEFORE INSERT OR UPDATE ON student_belegt_kurs
    FOR EACH ROW EXECUTE PROCEDURE num_tn_le_max_tn();
