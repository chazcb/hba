/*
rm repo.db
python model.py
python entrez_gene_update.py
sqlite3 repo.db < insert_test_data.sql 
*/

/*
INSERT INTO users (username, password, firstname, lastname, email, date_created )VALUES ('vivien', 'vivien', 'vivien', 'chan', 'vivienwchan@gmail.com', (SELECT datetime('now')) );
*/

INSERT INTO users VALUES (1, 'vivien', 'vivien', 'vivien', 'chan', 'vivienwchan@gmail.com', (SELECT datetime('now')) );
INSERT INTO users VALUES (2, 'kris', 'kris', 'kris', 'morrow', 'morrowkr02@gmail.com', (SELECT datetime('now')) );

INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (1, 1, 'HER2+ breast cancer', 'ERBB2+ subset from TCGA', "2014-07-08 23:01:53.561922", 1);
INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (2, 1, 'Triple negative breast cancer', 'TNBR subset from TCGA', "2014-07-08 23:01:53.561922", 0);
INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (3, 2, 'ER+ breast cancer', 'ER+ BrCa subset from TCGA', "2014-07-08 23:01:53.561922", 1);
INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (4, 2, 'TNBR', 'TCGA TNBR subset', "2014-07-08 23:01:53.561922", 0);

/* HER2+ : ERBB2, GRB7 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (1,1,1683); /* egeneid = 2064 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (2,1,2380); /* egeneid = 2886 */

/* ER+ : ESR1, PGR */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (3,3,1707); /* egeneid = 2099 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (4,3,4253); /* egeneid = 5241 */

/* TNBR: AGT, TP53 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (5,2,158); /* egeneid = 183 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (6,2,5881); /* egeneid = 7157 */

/* TNBR: CCL5, CLSPN */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (7,4,5169); /* egeneid = 6352 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (8,4,14318); /* egeneid = 63967 */

INSERT INTO tags (id, tag_text) VALUES (1, 'breast cancer');
INSERT INTO tags (id, tag_text) VALUES (2, 'HER2+ breast cancer');
INSERT INTO tags (id, tag_text) VALUES (3, 'Triple negative breast cancer');
INSERT INTO tags (id, tag_text) VALUES (4, 'ER+ breast cancer');
INSERT INTO tags (id, tag_text) VALUES (5, 'colon cancer');
INSERT INTO tags (id, tag_text) VALUES (6, 'colorectal cancer');
INSERT INTO tags (id, tag_text) VALUES (7, 'lung cancer');
INSERT INTO tags (id, tag_text) VALUES (8, 'lung adenocarcinoma');
INSERT INTO tags (id, tag_text) VALUES (9, 'sarcoma');
INSERT INTO tags (id, tag_text) VALUES (10, 'glioblastoma');
INSERT INTO tags (id, tag_text) VALUES (11, 'acute lymphocytic leukemia');
INSERT INTO tags (id, tag_text) VALUES (12, 'esophageal cancer');

INSERT INTO user_tag (id, tag_id, user_id) VALUES (1, 1, 1);
INSERT INTO user_tag (id, tag_id, user_id) VALUES (2, 1, 2);
INSERT INTO user_tag (id, tag_id, user_id) VALUES (3, 2, 1);
INSERT INTO user_tag (id, tag_id, user_id) VALUES (4, 3, 2);
INSERT INTO user_tag (id, tag_id, user_id) VALUES (5, 4, 3);

INSERT INTO list_tag (id, tag_id, list_id) VALUES (6, 1, 1);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (7, 1, 2);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (8, 1, 3);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (9, 2, 1);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (10, 3, 2);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (11, 4, 3);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (12, 1, 4);
INSERT INTO list_tag (id, tag_id, list_id) VALUES (13, 3, 4);

INSERT INTO collections (id, user_id, description, date_created) VALUES (1, 1, 'breast cancer collection', (SELECT datetime('now')) );

INSERT INTO list_collection (id, collection_id, list_id) VALUES (1, 1, 1);
INSERT INTO list_collection (id, collection_id, list_id) VALUES (2, 1, 2);
INSERT INTO list_collection (id, collection_id, list_id) VALUES (3, 1, 3);

/* list id 2, 4 are private, list_id 1, 2 owned by user_id 1, set list 2 accessible by user_id 2 */
INSERT INTO list_access (id, list_id, user_id) VALUES (1, 2, 2);
INSERT INTO list_access (id, list_id, user_id) VALUES (2, 4, 1);

CREATE VIEW V_USER_LISTS_GENES AS
SELECT 	u.username, 
		l.user_id, 
		l.id AS list_id, 
		l.title, 
		l.public, 
		g.id AS gene_rid, 
		g.entrez_gene_id AS egene_id, 
		g.entrez_gene_symbol AS egene_sym
FROM users u 
	INNER JOIN lists l ON (u.id = l.user_id)
	INNER JOIN list_gene lg ON (l.ID = lg.list_id)
	INNER JOIN genes g ON (lg.gene_id = g.id);

CREATE VIEW V_USER_LISTS_ACCESS AS
SELECT 	u.username, 
		l.id as list_id, 
		l.user_id AS owner_uid, 
		l.title, 
		l.public, 
		c.ct,
		a.user_id as shared_uid
FROM users u
	INNER JOIN lists l ON (u.id = l.user_id)
	INNER JOIN (SELECT list_id, count(gene_id) as CT FROM list_gene GROUP BY list_id) c 
		ON (l.id = c.list_id)
	LEFT OUTER JOIN list_access a on (l.id = a.list_id);

