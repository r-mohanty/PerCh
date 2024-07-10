from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
DATABASE_URL = "sqlite:///user_accounts.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    collection_name = Column(String, nullable=False)

# Create the database tables
Base.metadata.create_all(engine)

# Create a session maker bound to the engine
Session = sessionmaker(bind=engine)