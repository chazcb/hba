Week1:
Completed backend:
	- set up sqlite3 db
	- set up insert_test_data.sql script to populate with test data
	- designed schema - see schema_erd.png
	- set up model.py
	- set up controller: list_app.py, set up flask framework
	- wrote entrez_gene_update.py to populate genes table from NCBI ftp
Completed UI features:
	- set up base.html using css nav-bar styling
	- login.html page: set up error checking for non-existing or incorrect username or incorrect password
	- signup.html page: set up error checking for existing username or email address
	- user.html page: display user profile
	- downloaded ideogram html pages and depencencies from MD Anderson and integrated in Flask framework
	- set up bare bone index.html
	- view.html page: 
		- functional links to display ideogram for each list
		- ajax pop up to view gene details of list.onclick
			- added tablesorter.js to enable sorting using jQuery
		- display tags, date created and owner for list
	- started newlist.html

Week2 plan:
	- newlist page: file upload, new tags, modify schema to add column attributes in uploaded files
	- add user tags
	- generate list collection
	- give list access to collaborators
	- advanced search features: by gene, by tag (use hash in url?)
	- integrate mSigDB
	- integrate geneid history

Nice to haves:
	- tag cloud
	- heatmap.js on genomic view
	- lucene/solr/elasticsearch based search
