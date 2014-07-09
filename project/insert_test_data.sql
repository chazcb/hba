rm repo.db
python model.py
python entrez_gene_update.py

sqlite3 repo.db

INSERT INTO users VALUES (1, 'vivien', 'vivien', 'vivien', 'chan', 'vivienwchan@gmail.com', (SELECT datetime('now')) );
INSERT INTO users VALUES (2, 'kris', 'kris', 'kris', 'morrow', 'morrowkr02@gmail.com', (SELECT datetime('now')) );

INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (1, 1, 'HER2+ breast cancer', 'ERBB2+ subset from TCGA', "2014-07-08 23:01:53.561922", 1);
INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (2, 1, 'Triple negative breast cancer', 'TNBR subset from TCGA', "2014-07-08 23:01:53.561922", 0);
INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (3, 2, 'ER+ breast cancer', 'ER+ BrCa subset from TCGA', "2014-07-08 23:01:53.561922", 1);
INSERT INTO lists (id, user_id, title, description, date_created, public) VALUES (4, 2, 'TNBR', 'TCGA TNBR subset', "2014-07-08 23:01:53.561922", 0);

/* HER2+ : ERBB2, GRB7 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (1,1,2064);
INSERT INTO list_gene (id, list_id, gene_id) VALUES (2,1,2886);

/* ER+ : ESR1, PGR */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (3,3,2099);
INSERT INTO list_gene (id, list_id, gene_id) VALUES (4,3,5241);

/* TNBR: AGT, TP53 */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (5,2,183);
INSERT INTO list_gene (id, list_id, gene_id) VALUES (6,2,7157);

/* TNBR: CCL5, CLSPN */
INSERT INTO list_gene (id, list_id, gene_id) VALUES (7,4,6352);
INSERT INTO list_gene (id, list_id, gene_id) VALUES (8,4,63967);

INSERT INTO tags (id, tag_text) VALUES (1, 'breast cancer');
INSERT INTO tags (id, tag_text) VALUES (2, 'HER2+ breast cancer');
INSERT INTO tags (id, tag_text) VALUES (3, 'Triple negative breast cancer');
INSERT INTO tags (id, tag_text) VALUES (4, 'ER+ breast cancer');

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

INSERT INTO collections (id, user_id, description, date_created) VALUES (1, 1, 'breast cancer collection', "2014-07-08 23:01:53.561922");

INSERT INTO list_collection (id, collection_id, list_id) VALUES (1, 1, 1);
INSERT INTO list_collection (id, collection_id, list_id) VALUES (2, 1, 2);
INSERT INTO list_collection (id, collection_id, list_id) VALUES (3, 1, 3);

/* list id 2, 4 are private, list_id 1, 2 owned by user_id 1, set list 2 accessible by user_id 2 */
INSERT INTO list_access (id, list_id, user_id) VALUES (1, 2, 2);
