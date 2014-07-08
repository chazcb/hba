from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

ENGINE = create_engine("sqlite:///repo.db", echo=True)
db_session = scoped_session(sessionmaker(bind=ENGINE,
                                       autocommit = False,
                                       autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()

### Class declarations 
# entity classes
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False)
    password = Column(String(50), nullable = False)
    firstname = Column(String(50), nullable = True)
    lastname = Column(String(50), nullable = True)
    email = Column(String(50), nullable = True)

class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key = True)
    entrez_gene_id = Column(Integer, nullable = False)
    entrez_gene_symbol = Column(String(50), nullable = True)
    entrez_gene_synonym = Column(String(255), nullable = True)
    entrez_gene_desc = Column(String(255), nullable = True)
    entrez_version = Column(DateTime, nullable = False)

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    title = Column(String(255), nullable = True)
    description = Column(String(255), nullable = True)
    public = Column(Boolean, default = False)
    date_created = Column(DateTime, nullable = False)
    file_obj = Column(Text, nullable = True)

    user = relationship("User",
            backref=backref("lists", order_by=id))

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    description = Column(String(255), nullable = True)
    date_created = Column(DateTime, nullable = False)

    user = relationship("User",
            backref=backref("collections", order_by=id))

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key = True)
    tag_text = Column(String(255), nullable = False)

# cross tables

class User_tag(Base):
    __tablename__ = "user_tag"

    id = Column(Integer, primary_key = True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

    tag = relationship("Tag",
            backref=backref("user_tag", order_by=id))
    user = relationship("User",
            backref=backref("user_tag", order_by=id))

class List_tag(Base):
    __tablename__ = "list_tag"

    id = Column(Integer, primary_key = True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable = False)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)

    tag = relationship("Tag",
            backref=backref("list_tag", order_by=id))
    lists = relationship("List",
            backref=backref("list_tag", order_by=id))

class List_access(Base):
    __tablename__ = "list_access"

    id = Column(Integer, primary_key = True)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

    lists = relationship("List",
            backref=backref("list_access", order_by=id))
    user = relationship("User",
            backref=backref("list_access", order_by=id))

class List_user(Base):
    __tablename__ = "list_user"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)

    user = relationship("User",
            backref=backref("list_user", order_by=id))
    lists = relationship("List",
            backref=backref("list_user", order_by=id))

class List_gene(Base):
    __tablename__ = "list_gene"

    id = Column(Integer, primary_key = True)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)
    gene_id = Column(Integer, ForeignKey('genes.id'), nullable = False)

    lists = relationship("List",
            backref=backref("list_gene", order_by=id))
    gene = relationship("Gene",
            backref=backref("list_gene", order_by=id))

class List_collection(Base):
    __tablename__ = "list_collection"

    id = Column(Integer, primary_key = True)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable = False)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable = False)

    collection = relationship("Collection",
            backref=backref("list_collection", order_by=id))
    lists = relationship("List",
            backref=backref("list_collection", order_by=id))

### End class declarations

def main():

    # initialize database
    Base.metadata.create_all(ENGINE)

if __name__ == "__main__":
    main()
