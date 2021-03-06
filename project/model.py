from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
# import sqlite3

ENGINE = create_engine("sqlite:///repo.db", echo=False)
db_session = scoped_session(sessionmaker(bind=ENGINE,
                                       autocommit = False,
                                       autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()

### Class declarations 

# entity classes
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement=True)
    username = Column(String(50), nullable = False)
    password = Column(String(50), nullable = False)
    firstname = Column(String(50), nullable = True)
    lastname = Column(String(50), nullable = True)
    email = Column(String(50), nullable = True)
    date_created = Column(DateTime, nullable = False)

class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key = True, autoincrement=True)
    entrez_gene_id = Column(Integer, nullable = False)
    entrez_gene_symbol = Column(String(50), nullable = True)
    entrez_gene_synonym = Column(String(255), nullable = True)
    entrez_gene_desc = Column(String(255), nullable = True)

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    title = Column(String(255), nullable = True)
    description = Column(String(255), nullable = True)
    url = Column(String(255), nullable = True)
    public = Column(Boolean, default = False, nullable = False)
    filename = Column(String(255), nullable = True)
    file_obj = Column(Text, nullable = True)
    date_created = Column(DateTime, nullable = False)    

    user = relationship("User",
            backref=backref("lists", order_by=id))

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    description = Column(String(255), nullable = True)
    date_created = Column(DateTime, nullable = False)

    user = relationship("User",
            backref=backref("collections", order_by=id))

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key = True, autoincrement=True)
    tag_text = Column(String(255), nullable = False)

class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key = True)
    url = Column(String(255), nullable = False)
    timestamp = Column(DateTime, nullable = False)

# cross tables

class userTag(Base):
    __tablename__ = "user_tag"

    id = Column(Integer, primary_key = True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

    tag = relationship("Tag",
            backref=backref("user_tag", order_by=id))
    user = relationship("User",
            backref=backref("user_tag", order_by=id))

class listTag(Base):
    __tablename__ = "list_tag"

    id = Column(Integer, primary_key = True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable = False)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)

    tag = relationship("Tag",
            backref=backref("list_tag", order_by=id))
    lists = relationship("List",
            backref=backref("list_tag", order_by=id))

class listAccess(Base):
    __tablename__ = "list_access"

    id = Column(Integer, primary_key = True, autoincrement=True)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

    lists = relationship("List",
            backref=backref("list_access", order_by=id))
    user = relationship("User",
            backref=backref("list_access", order_by=id))

class listGene(Base):
    __tablename__ = "list_gene"

    id = Column(Integer, primary_key = True, autoincrement=True)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)
    gene_id = Column(Integer, ForeignKey('genes.id'), nullable = False)

    lists = relationship("List",
            backref=backref("list_gene", order_by=id))
    gene = relationship("Gene",
            backref=backref("list_gene", order_by=id))

class listCollection(Base):
    __tablename__ = "list_collection"

    id = Column(Integer, primary_key = True, autoincrement=True)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable = False)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)

    collection = relationship("Collection",
            backref=backref("list_collection", order_by=id))
    lists = relationship("List",
            backref=backref("list_collection", order_by=id))

class geneVersion(Base):
    __tablename__ = "gene_version"

    id = Column(Integer, primary_key = True, autoincrement=True)
    gene_id = Column(Integer, ForeignKey('genes.id'), nullable = False)
    version_id = Column(Integer, ForeignKey('versions.id'), nullable = False)

    gene = relationship("Gene",
            backref=backref("gene_version", order_by=id))

    version = relationship("Version",
            backref=backref("gene_version", order_by=id))

# table for storing temp data for validation

class tempGene(Base):
    __tablename__ = "tempgenes"

    id = Column(Integer, primary_key = True, autoincrement=True)
    row_num = Column(Integer, nullable = False)
    temp_gene_id = Column(Integer, nullable = False)
    stamp = Column(String(50), nullable = False)

### End class declarations

### functions:

# def connect():
#     conn = sqlite3.connect("repo.db")
#     cursor = conn.cursor()
#     return cursor

def get_attr_max(db_session, class_attr, default = 0):

    max_val = db_session.query(func.max(class_attr)).one()[0]
    
    if max_val:
        return max_val
    else:
        return default

# def sql_get_attr_max(attr, table):

#     cursor = connect()
#     query = "SELECT max(?) from ?;"
#     cursor.execute(query, (attr, table))
#     attr_max = cursor.fetchone()

#     return attr_max 

def main():

    # initialize database
    Base.metadata.create_all(ENGINE)
    # pass

if __name__ == "__main__":
    main()
