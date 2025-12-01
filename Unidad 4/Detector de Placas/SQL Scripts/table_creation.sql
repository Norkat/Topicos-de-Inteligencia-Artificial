
-- Owners table
-- SELECT * FROM owners;
-- DROP TABLE owners;
-- TRUNCATE TABLE owners;
CREATE TABLE IF NOT EXISTS owners (
	owner_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	owner_first_name TEXT NOT NULL,
	owner_last_name TEXT NOT NULL,
	owner_email TEXT NOT NULL,
	owner_phone VARCHAR(20) NOT NULL
);

-- Cars table
-- SELECT * FROM cars;
-- DROP TABLE cars;
-- TRUNCATE TABLE cars;
CREATE TABLE IF NOT EXISTS cars (
	licence_plate TEXT PRIMARY KEY,
	car_model TEXT NOT NULL,
	car_brand TEXT NOT NULL,
	car_year TEXT NOT NULL,
	car_color TEXT NOT NULL,
    car_owner_id UUID REFERENCES owners(owner_id) NOT NULL
);