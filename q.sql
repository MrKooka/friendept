CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  name TEXT
);

CREATE TABLE debt_record (
  id INTEGER PRIMARY KEY,
  amount REAL,
  debtor INTEGER,
  creditor INTEGER,
  author TEXT,
  datetime DATETIME,
  author_id INTEGER,
  confirmation bool,
  comment TEXT
  FOREIGN KEY (debtor) REFERENCES user(id),
  FOREIGN KEY (creditor) REFERENCES user(id)
);
