Use mydb;



CREATE TRIGGER delete_old_reservations
AFTER INSERT ON demo_review
FOR EACH ROW
BEGIN
     /* FROM demo_reservation */
    DELETE FROM demo_reservation
    WHERE reservation_date < DATE_SUB(NOW(), INTERVAL 5 DAY);
END //


DELIMITER ;
DROP TRIGGER IF EXISTS delete_min_rating;

CREATE TRIGGER delete_min_rating
AFTER INSERT ON demo_review
FOR EACH ROW
BEGIN
     /* FROM demo_reservation */
    IF NEW.rating < 3
    THEN 
    DELETE FROM demo_reservation
    WHERE book_id = NEW.book_id AND user_id = NEW.user_id;
    END IF;
END //