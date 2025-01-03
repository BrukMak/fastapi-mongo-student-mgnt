from bson.objectid import ObjectId
import motor.motor_asyncio 
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")

# helper function to convert MongoDB document to Python dictionary

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "course": student["course"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# Retrieve all students present in the database
async def retrieve_students() -> list: 
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))

    return students

# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)

# Retrieve a student with an ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)
    return None

# Update a student with an ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        update_student = await student_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if update_student:
            return True
        return False
# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    print(student)
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
