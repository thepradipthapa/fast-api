from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgresadmin@localhost:5432/fastapi_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Database connection
# try:
#     conn = psycopg2.connect(
#         host='localhost', 
#         database='fastapi_db', 
#         user='postgres', 
#         password='postgresadmin', 
#         cursor_factory=RealDictCursor
#         )
#     cursor = conn.cursor()
#     print("Database connection was successfull!")
# except Exception as error:
#     print("Database connectin failed!")
#     print("Error :", error)
#     time.sleep(2)
