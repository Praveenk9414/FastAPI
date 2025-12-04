# CRUD operations / HTTP requests

# Create - POST
# Read - GET
# Update - PUT
# Delete - DELETE

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

# creating an fastapi obj
app = FastAPI(title="Integration with sql")

# Database setup
engine = create_engine("sqlite:///students.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()




# Database Model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    year = Column(Integer, nullable=False)

# Now after creating a model (basically an sql table) ... our model need to speak to the engine
Base.metadata.create_all(engine)


# Pydantic Models (Dataclass)
class StudentCreate(BaseModel):
    name:str
    dept:str
    email:str
    year:int

class StudentResponse(BaseModel):
    id:int
    name:str
    dept:str
    email:str
    year:int

    class config:
        from_attributes = True
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()


# Endpoints
@app.get("/")
def root():
    return {"message": "FastAPI with sql"}

# View existing students data
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id:int, db:Session = Depends(get_db)):
    stud = db.query(Student).filter(Student.id == student_id).first()
    if not stud:
        raise HTTPException(status_code=404, detail="Student not found!")
    return stud

# Add new students data
@app.post("/students/", response_model=StudentResponse)
def create_student(stud: StudentCreate, db:Session = Depends(get_db)):
    if db.query(Student).filter(Student.email == stud.email).first():
        raise HTTPException(status_code=404, detail="Student already exists!")
    
    # create a new student
    new_stud = Student(**stud.model_dump())
    db.add(new_stud)
    db.commit()
    db.refresh(new_stud)
    return new_stud

# Update Students data
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id:int, student:StudentCreate, db:Session = Depends(get_db)):
    db_stud = db.query(Student).filter(Student.id == student_id).first()
    if not db_stud:
        raise HTTPException(status_code=404, detail="Student doesn't exist!")
    
    for field, value in student.model_dump().items():
        setattr(db_stud, field, value)
    
    db.commit()
    db.refresh(db_stud)
    return db_stud

    
# Delete Students data
@app.delete("/students/{student_id}")
def delete_student(student_id:int, db:Session = Depends(get_db)):
    db_stud = db.query(Student).filter(Student.id == student_id).first()
    if not db_stud:
        raise HTTPException(status_code=404, detail="Student doesn't exist!")
    
    db.delete(db_stud)
    db.commit()
    return {"message":"Student Deleted"}


# Get all students
@app.get("/students/", response_model=List[StudentResponse])
def get_all_students(db:Session = Depends(get_db)):
    return db.query(Student).all()