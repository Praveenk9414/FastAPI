from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import StudentCreate, StudentResponse
from models import Student

router = APIRouter(
    prefix="/students",
    tags=["students"],
)


# CRUD operations / HTTP requests

# Create - POST
# Read - GET
# Update - PUT
# Delete - DELETE

# Get all students
@router.get("/", response_model=List[StudentResponse])
def get_all_students(db:Session = Depends(get_db)):
    return db.query(Student).all()

# View existing students data
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id:int, db:Session = Depends(get_db)):
    stud = db.query(Student).filter(Student.id == student_id).first()
    if not stud:
        raise HTTPException(status_code=404, detail="Student not found!")
    return stud

# Filter students record based on Year and Dept
@router.get("/students/filter", response_model=List[StudentResponse])
def get_filter_record(dept:str, year:int, db:Session = Depends(get_db)):

    students = db.query(Student).filter(Student.dept == dept,
                                        Student.year == year).all()
    return students


# Add new students data
@router.post("/", response_model=StudentResponse)
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
@router.put("/{student_id}", response_model=StudentResponse)
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
@router.delete("/{student_id}")
def delete_student(student_id:int, db:Session = Depends(get_db)):
    db_stud = db.query(Student).filter(Student.id == student_id).first()
    if not db_stud:
        raise HTTPException(status_code=404, detail="Student doesn't exist!")
    
    db.delete(db_stud)
    db.commit()
    return {"message":"Student Deleted"}
