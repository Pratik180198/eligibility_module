from pydantic import BaseModel
from fastapi import Form
from typing import List


class UserDetails(BaseModel):
    full_name: str
    email_id: str
    graduation_completed: str
    stream: str
    cgpa: float
    entrance_exam_score: int

    @classmethod
    def as_form(cls, full_name: str = Form(...),
                email_id: str = Form(...),
                graduation_completed: str = Form(...),
                stream: str = Form(...),
                cgpa: float = Form(...),
                entrance_exam_score: int = Form(...)):
        return cls(full_name=full_name, email_id=email_id, graduation_completed=graduation_completed,
                   stream=stream, cgpa=cgpa,
                   entrance_exam_score=entrance_exam_score)

    class Config:
        orm_mode = True


class StageOne(BaseModel):
    graduation_completed: str

    @classmethod
    def as_form(cls, graduation_completed: str = Form(...)):
        return cls(graduation_completed=graduation_completed)

    class Config:
        orm_mode = True


class StageTwo(BaseModel):
    stream: List[str]

    @classmethod
    def as_form(cls, stream: List[str] = Form(...)):
        return cls(stream=stream)

    class Config:
        orm_mode = True


class StageThree(BaseModel):
    cgpa_one: float
    cgpa_two: float

    @classmethod
    def as_form(cls, cgpa_one: float = Form(...),
                cgpa_two: float = Form(...)):
        return cls(cgpa_one=cgpa_one, cgpa_two=cgpa_two)

    class Config:
        orm_mode = True


class StageFour(BaseModel):
    ent_one: int
    ent_two: int

    @classmethod
    def as_form(cls, ent_one: int = Form(...),
                ent_two: int = Form(...)):
        return cls(ent_one=ent_one, ent_two=ent_two)

    class Config:
        orm_mode = True
