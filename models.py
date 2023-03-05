from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base


class Patients(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patientId = Column(String)
    dob = Column(Date)
    confusion = Column(Boolean)
    urea = Column(Integer)
    respiratory = Column(Integer)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    score = Column(Integer)