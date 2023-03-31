-- migrate:up
CREATE TABLE restaurants (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  operating_hours TEXT NOT NULL
);

CREATE TABLE operating_time (
  id SERIAL PRIMARY KEY,
  restaurant_id INTEGER REFERENCES Restaurants(id),
  start_min INTEGER NOT NULL,
  end_min INTEGER NOT NULL
);

-- migrate:down
DROP TABLE operating_hours
DROP TABLE restaurnatns

