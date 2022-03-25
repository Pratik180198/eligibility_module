from database import Base
from sqlalchemy import Column, Integer, String, Float


class StudentTable(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(30))
    email_id = Column(String(50), unique=True)
    graduation_completed = Column(String(30))
    stream = Column(String(30))
    cgpa = Column(Float(10))
    entrance_exam_score = Column(Integer)


class StageOneTable(Base):
    __tablename__ = 'stage_one'
    id = Column(Integer)
    full_name = Column(String(30))
    email_id = Column(String(50), primary_key=True, index=True)
    graduation_completed = Column(String(30))
    stream = Column(String(30))
    cgpa = Column(Float(10))
    entrance_exam_score = Column(Integer)


class StageTwoTable(Base):
    __tablename__ = 'stage_two'
    id = Column(Integer)
    full_name = Column(String(30))
    email_id = Column(String(50), primary_key=True, index=True)
    graduation_completed = Column(String(30))
    stream = Column(String(30))
    cgpa = Column(Float(10))
    entrance_exam_score = Column(Integer)
