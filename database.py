from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine("sqlite:///students.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Now after creating a model (basically an sql table) ... our model need to speak to the engine
Base.metadata.create_all(engine)

    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()