from pydantic import BaseModel

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