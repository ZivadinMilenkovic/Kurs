from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password?@<ip_adress/hostname>/<database name>


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.datebase_username}:{settings.datebase_passoword}@{settings.datebase_hostname}/{settings.datebase_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"options": "-c timezone=utc"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def for_sql():
#     while True:
#         try:
#             conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="postgres",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("database connection wasa succesfull")
#         break
#         except Exception as error:
#             print("connecting to database fail")
#             print("Error", error)
#             time.sleep(2)
