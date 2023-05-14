CREATE TABLE word_count (
	id SERIAL PRIMARY KEY,
	word varchar(500) UNIQUE NOT NULL,
	count integer NOT NULL
);