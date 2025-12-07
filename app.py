
from fastapi import FastAPI, HTTPException, Depends
from database import Base, engine
from routes import students

# creating an fastapi obj
app = FastAPI(title="Integration with sql")


@app.get("/")
def root():
    return {"message": "FastAPI with sql"}

app.include_router(students.router)