CREATE TABLE apps
(
	id TEXT PRIMARY KEY
);

CREATE TABLE uids
(
	id TEXT PRIMARY KEY
);

CREATE TABLE uidToAppUsage
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid TEXT,
	app_id TEXT,
	usagestamp TEXT,
	duration TEXT,
	tf TEXT,
	app_signature TEXT,
	FOREIGN KEY (uid) REFERENCES uids(id),
	FOREIGN KEY (app_id) REFERENCES apps(id)
);

CREATE TABLE uidToDevices
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid TEXT,
	device_id TEXT,
	FOREIGN KEY (uid) REFERENCES uids(id)
);


CREATE TABLE eboxes
(
	id TEXT PRIMARY KEY
)