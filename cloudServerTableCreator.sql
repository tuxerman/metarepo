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
	eboxid TEXT,
	FOREIGN KEY (uid) REFERENCES uids(id),
	FOREIGN KEY (app_id) REFERENCES apps(id),
	FOREIGN KEY (eboxid) REFERENCES eboxes(id)
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
);

CREATE TABLE eboxesToUids
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	eboxid TEXT,
	uid TEXT,
	FOREIGN KEY (uid) REFERENCES uids(id),
	FOREIGN KEY (eboxid) REFERENCES eboxes(id)
);

CREATE TABLE eboxesToApps
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	eboxid TEXT,
	app_id TEXT,
	FOREIGN KEY (app_id) REFERENCES apps(id),
	FOREIGN KEY (eboxid) REFERENCES eboxes(id)
);
