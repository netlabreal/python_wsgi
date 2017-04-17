CREATE TABLE regions (id INTEGER PRIMARY KEY, name VARCHAR(100));
CREATE TABLE towns (id INTEGER PRIMARY KEY, rid INTEGER KEY, name VARCHAR(100));
CREATE TABLE comments (id INTEGER PRIMARY KEY, fam VARCHAR(100), name VARCHAR(100), otch VARCHAR(100), region INTEGER KEY, town INTEGER KEY, tel VARCHAR(15), email VARCHAR(20), comment VARCHAR(300));

INSERT INTO regions(name) VALUES ("Краснодарский край");
INSERT INTO regions(name) VALUES ("Ростовская область");
INSERT INTO regions(name) VALUES ("Ставропольский край");

INSERT INTO towns(rid, name) VALUES (1, "Краснодар");
INSERT INTO towns(rid, name) VALUES (1, "Кропоткин");
INSERT INTO towns(rid, name) VALUES (1, "Славянск");

INSERT INTO towns(rid, name) VALUES (2, 'Ростов');
INSERT INTO towns(rid, name) VALUES (2, 'Шахты');
INSERT INTO towns(rid, name) VALUES (2, 'Батайск');

INSERT INTO towns(rid, name) VALUES (3, 'Ставрополь');
INSERT INTO towns(rid, name) VALUES (3, 'Пятигорск');
INSERT INTO towns(rid, name) VALUES (3, 'Кисловодск');



INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит', 'Алекс', 'Бор', 1, 1, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит1', 'Алекс1', 'Бор1', 1, 1, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит2', 'Алекс2', 'Бор2', 1, 1, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит3', 'Алекс3', 'Бор3', 1, 1, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит4', 'Алекс4', 'Бор4', 1, 1, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит5', 'Алекс5', 'Бор5', 1, 1, '(495)5789213', 'l@l.ru','**********************');

INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Литт', 'Алекс', 'Бор', 1, 2, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Литт1', 'Алекс1', 'Бор1', 1, 2, '(495)5789213', 'l@l.ru','**********************');

INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Литтт', 'Алекс', 'Бор', 1, 3, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Литтт1', 'Алекс1', 'Бор1', 1, 3, '(495)5789213', 'l@l.ru','**********************');


INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит', 'Алекс', 'Бор', 2, 4, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит1', 'Алекс1', 'Бор1', 2, 4, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит2', 'Алекс2', 'Бор2', 2, 4, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит3', 'Алекс3', 'Бор3', 2, 4, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит4', 'Алекс4', 'Бор4', 2, 4, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит5', 'Алекс5', 'Бор5', 2, 4, '(495)5789213', 'l@l.ru','**********************');



INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит', 'Алекс', 'Бор', 3, 8, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит1', 'Алекс1', 'Бор1', 3, 8, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит2', 'Алекс2', 'Бор2', 3, 8, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит3', 'Алекс3', 'Бор3', 3, 8, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит4', 'Алекс4', 'Бор4', 3, 8, '(495)5789213', 'l@l.ru','**********************');
INSERT INTO comments(fam, name, otch, region, town, tel, email, comment) VALUES ('Лит5', 'Алекс5', 'Бор5', 3, 8, '(495)5789213', 'l@l.ru','**********************');
