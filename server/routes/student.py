from fastapi import APIRouter, HTTPException, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_students,
    add_student,
    retrieve_student,
    update_student,
    delete_student
)
from server.models.student import (
    StudentSchema,
    UpdateStudentModel,
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()

# Add a new student to the database
@router.post("/", response_description="Student data added into the databaes")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully")

# Retrieve all students from the database
@router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")

# Retrieve a student with an ID
@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await retrieve_student(id)
    print(student)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

# Update a student with an ID
@router.put("/{id}", response_description="Student data updated")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    student = await retrieve_student(id)
    if student:
        new_data = {k:v for k, v in req.dict().items() if v }
        updated_student = await update_student(id, new_data)
        if updated_student:
            return ResponseModel(updated_student, "Student with ID {} value updated successfully".format(id))
        return ErrorResponseModel("An error occurred", 404, "There was an error updating the student data.")
    return ErrorResponseModel("An error occurred", 404, "Student doesn't exist.")

# Delete a student from the database
@router.delete("/{id}", response_description = "Student data deleted from the database")
async def delete_student_data(id: str):
    found = await delete_student(id)
    if found:
        return ResponseModel("Student with ID {} removed".format(id), "Student deleted successfully")
    return ErrorResponseModel("An error occurred", 404, "Student with ID {} doesn't exist".format(id))
