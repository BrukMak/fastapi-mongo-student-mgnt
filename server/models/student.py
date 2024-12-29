from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# StudentModel will be used to validate the request body when creating a new student
class StudentSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    course : str = Field(...)
    year : int = Field(..., ge=1, lt=9)
    gpa : float = Field(..., gt=0.0, lt=4.0)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Bruk Mak",
                "email": "bruk@a2sv.org",
                "course": "Web Development",
                "year": 3,
                "gpa": 3.6
            }
        }

# UpdateStudentModel will be used to update the student details not only fully but also partially that why all fields are optional
class UpdateStudentModel(BaseModel):
    name : Optional[str]
    email : Optional[EmailStr]
    course : Optional[str]
    year : Optional[int]
    gpa : Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "name": "Bruk Mak",
                "email": "bruk@a2sv.org",
                "course": "Mobile Development",
                "year": 4,
                "gpa": 3.6
            }
        }
    
# to have consistent success and error responses, we will create a helper function to return the response
def ResponseModel(data, message):
    return  {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
