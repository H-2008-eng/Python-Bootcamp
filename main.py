from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Dict,Optional,List

app = FastAPI()

class PersonalInformation(BaseModel):
    name: str
    age: int
    gender: str
    contact_number: int
    address: str
    email: Optional[str] = None

class AcademicHistory(BaseModel):
    current_grade: int
    english: float
    urdu: float
    maths: float
    science: float
    academic_percentage: float | None = None

class AttendanceHistory(BaseModel):
    total_days: int
    attend_days: int
    attendance_percentage:  float | None = None

class Healthy(BaseModel):
    blood_type: Optional[str] = None
    emergency_number: int

class Participate(BaseModel):
    Events: Optional[str] = None
    sports: Optional[str] = None
    activities: Optional[str] = None

class Student(BaseModel):
    id_number: int
    personal_information:PersonalInformation
    academic_history:AcademicHistory
    attendance_history:AttendanceHistory
    healthy:Healthy
    participate:Participate

def calculate_total_percentage(academic:AcademicHistory):
    total = (
        academic.english +
        academic.urdu +
        academic.maths +
        academic.science
    )
    return round(total/4,2)

def calculate_attendance_percentage(attendance:AttendanceHistory):
    if attendance.attend_days == 0:
        return 0
    present = round((attendance.attend_days/attendance.total_days)*100,2)
    return present

total_students: Dict[int, Student] = {}

# @app.post("/students/",response_model=Student)
# def create_student(student:Student):
#     if student.id_number in total_students:
#         raise
#     HTTPException(status_code=404,detail="This id is already exist")
#     student.academic_history.academic_percentage = calculate_total_percentage(student.academic_history)
#     student.attendance_history.attendance_percentage = calculate_attendance_percentage(student.attendance_history)
#     total_students[student.id_number] = student
#     return student

# @app.get("/students/",response_model=List[Student])
# def get_all_students():
#     return list(total_students.values())

# @app.get("/students?{student_id}",response_model=Student)
# def get_student(student_id: int):
#     if student_id not in total_students:
#         raise
#     HTTPException(status_code=404,detial="Student not found")
#     return total_students[student_id]

# @app.put("/students/{student_id}",response_model=Student)
# def update_student(student_id: int,updated_student:Student):
#     if student_id not in total_students:
#         raise
#     HTTPException(status_code=404,detail="Student not found")
#     updated_student.academic_history.academic_percentage = calculate_total_percentage(updated_student.academic_history)
#     updated_student.attendance_history.attendance_percentage = calculate_attendance_percentage(updated_student.attendance_history)
#     total_students[student_id] = updated_student
#     return updated_student

# @app.delete("/students/{student_id}")
# def delete_student(student_id: int):
#     if student_id not in total_students:
#         raise
#     HTTPException(status_code=404,detail="student not found")
#     del total_students[student_id]
#     return{"message":"student delete successfully"}

@app.post("/students/", response_model=Student)
def create_student(student: Student):
    if student.id_number in total_students:
        raise HTTPException(status_code=400, detail="This id already exists")

    student.academic_history.academic_percentage = calculate_total_percentage(student.academic_history)
    student.attendance_history.attendance_percentage = calculate_attendance_percentage(student.attendance_history)
    total_students[student.id_number] = student
    return student


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id not in total_students:
        raise HTTPException(status_code=404, detail="Student not found")
    return total_students[student_id]


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    if student_id not in total_students:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student.academic_history.academic_percentage = calculate_total_percentage(updated_student.academic_history)
    updated_student.attendance_history.attendance_percentage = calculate_attendance_percentage(updated_student.attendance_history)
    total_students[student_id] = updated_student
    return updated_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in total_students:
        raise HTTPException(status_code=404, detail="Student not found")

    del total_students[student_id]
    return {"message": "Student deleted successfully"}
