from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/demo_fastapi"
# DATABASE_URL = "mysql+mysqlconnector://uj2e9efqtud9o1kj:RgQUFdSt8kwpoS0hOQ1o@bbkpqybvi5txep4qrdcb-mysql.services.clever-cloud.com:3306/bbkpqybvi5txep4qrdcb"
# engine = create_engine(DATABASE_URL)  # creating engine
SQLALCHAMY_DB_URL = 'mysql+mysqlconnector://uvayh5ymlkx8ybfd:HJEYCKFKknzzlP7cvlKL@bjylablqdhnmt0gvpyai-mysql.services.clever-cloud.com:3306/bjylablqdhnmt0gvpyai'

engine = create_engine(SQLALCHAMY_DB_URL)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
