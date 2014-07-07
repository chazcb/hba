from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation

ENGINE = create_engine("sqlite:///repo.db", echo=False)
db_session = scoped_session(sessionmaker(bind=ENGINE,
                                       autocommit = False,
                                       autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(50), nullable = True)
    username = Column(String(50), nullable = True)
    password = Column(String(50), nullable = True)
    firstname = Column(String(50), nullable = True)
    lastname = Column(String(50), nullable = True)

class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key = True)
    entrez_gene_id = Column(Integer, nullable = False)
    entrez_gene_symbol = Column(String(50), nullable = True)
    entrez_gene_desc = Column(String(255), nullable = True)
    entrez_version = Column(DateTime, nullable = False)

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key = True)
    title = Column(String(50), nullable = True)
    description = Column(String(255), nullable = True)
    date_created = Column(DateTime, nullable = False)
    file_loc = Column(String(255), nullable = False)

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_created = Column(DateTime, nullable = False)

    user = relationship("User",
            backref=backref("collections", order_by=id))

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key = True)
    tag_text = description = Column(String(255), nullable = False)

# cross tables

    __tablename__ = "tag_x_user"

    id = Column(Integer, primary_key = True)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    tag = relationship("Tag",
            backref=backref("tag_x_user", order_by=id))
    user = relationship("User",
            backref=backref("tag_x_user", order_by=id))

    __tablename__ = "tag_x_list"

    id = Column(Integer, primary_key = True)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    list_id = Column(Integer, ForeignKey('lists.id'))

    tag = relationship("Tag",
            backref=backref("tag_x_list", order_by=id))
    lists = relationship("List",
            backref=backref("tag_x_list", order_by=id))

    __tablename__ = "list_x_access"

    id = Column(Integer, primary_key = True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    lists = relationship("List",
            backref=backref("list_x_access", order_by=id))
    user = relationship("User",
            backref=backref("list_x_access", order_by=id))

    __tablename__ = "user_x_list"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    list_id = Column(Integer, ForeignKey('lists.id'))

    user = relationship("User",
            backref=backref("user_x_list", order_by=id))
    lists = relationship("List",
            backref=backref("user_x_list", order_by=id))

    __tablename__ = "list_x_gene"

    id = Column(Integer, primary_key = True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    gene_id = Column(Integer, ForeignKey('genes.id'))

    lists = relationship("List",
            backref=backref("list_x_gene", order_by=id))
    gene = relationship("Gene",
            backref=backref("list_x_gene", order_by=id))

    __tablename__ = "user_x_list"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    list_id = Column(Integer, ForeignKey('lists.id'))

    user = relationship("User",
            backref=backref("user_x_list", order_by=id))
    lists = relationship("List",
            backref=backref("user_x_list", order_by=id))

    __tablename__ = "collection_x_list"

    id = Column(Integer, primary_key = True)
    collection_id = Column(Integer, ForeignKey('collections.id'))
    list_id = Column(Integer, ForeignKey('lists.id'))

    collection = relationship("Collection",
            backref=backref("collection_x_list", order_by=id))
    lists = relationship("List",
            backref=backref("collection_x_list", order_by=id))


### End class declarations

# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///repo.db", echo=False)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()


def main():
    pass

if __name__ == "__main__":
    main()
