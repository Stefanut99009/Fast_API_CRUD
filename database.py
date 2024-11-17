from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database URL for MySQL
URL_DATABASE = "mysql+pymysql://root@localhost:3306/blog_application"

# Create the engine without 'connect_args'
engine = create_engine(URL_DATABASE)

# Create session and base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
