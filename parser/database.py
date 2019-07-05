from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, TIMESTAMP, Boolean, create_engine
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///database.db', convert_unicode=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class ReviewModel(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    author_id = Column(String)
    author_name = Column(String)
    author_profession = Column(SmallInteger)
    stars = Column(SmallInteger)
    datetime = Column(TIMESTAMP)
    text = Column(String)
    like = Column(SmallInteger)
    dislike = Column(SmallInteger)

    response_flag = Column(Boolean)
    response_title = Column(String)
    response_datetime = Column(String)
    response_text = Column(String)

    __table_args__ = (
        UniqueConstraint(
            "author_id",
            "author_name",
            "datetime",
            name="_review_uniq",
        ),
    )

Base.metadata.create_all(bind=engine)