-- CREATE the schema kkphim
CREATE SCHEMA IF NOT EXISTS kkphim;

CREATE TABLE IF NOT EXISTS kkphim.items (
    modified_time TIMESTAMP,
    _id VARCHAR,
    name VARCHAR,
    slug VARCHAR,
    origin_name VARCHAR,
    poster_url VARCHAR,
    thumb_url VARCHAR,
    year INT
);

ALTER TABLE kkphim.items
ALTER COLUMN year TYPE varchar(4);