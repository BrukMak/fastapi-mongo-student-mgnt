from fastapi import FastAPI
from server.routes.student import router as StudentRounter

app = FastAPI()
app.include_router(StudentRounter, tags=["Student"], prefix="/student")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Student Management System!"}