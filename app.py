from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

class Patient(BaseModel):
    patientId: str = Field(min_length=1)
    dob: date
    confusion: bool
    urea: int = Field(gt=-1)
    respiratory: int = Field(gt=-1)
    systolic: int = Field(gt=-1)
    diastolic: int = Field(gt=-1)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_mbp(systolic: int, diastolic: int):
    return diastolic + 1/3 * (systolic - diastolic)

def get_age(dob):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def get_score(pat: Patient):
    age = 1 if get_age(pat.dob) > 64 else 0
    mbp = 1 if get_mbp(pat.systolic, pat.diastolic) < 1.5 else 0
    conf = 1 if pat.confusion else 0
    urea = 1 if pat.urea > 19 else 0
    resp = 1 if pat.respiratory > 29 else 0
    score = age + mbp + conf + urea + resp
    return score


@app.get("/")
def list_patients(request: Request, db: Session = Depends(get_db)):
    #return db.query(models.Patients).all()
    return templates.TemplateResponse("index.html", {"request": request, "patients": db.query(models.Patients).all()})
    

@app.get("/search/{patient_id}")
def get_one(request: Request, patient_id: str, db: Session = Depends(get_db)):

    patients = db.query(models.Patients).filter(models.Patients.patientId == patient_id)
    
    if patients is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} Does not exist"
        )

    return templates.TemplateResponse("index.html", {"request": request, "patients": patients})


@app.post("/", response_class=HTMLResponse)
def new_patient(request: Request, db: Session = Depends(get_db), pid : str = Form(), dob : date = Form(), confusion : bool = Form(), urea : int = Form(), respiratory : int = Form(), systolic : int = Form(), diatolic : int = Form()):
    patient = db.query(models.Patients).filter(models.Patients.patientId == pid).first()
    if patient is None: 
        patient_model = models.Patients()
        patient_model.patientId = pid
        patient_model.dob = dob
        patient_model.confusion = confusion
        patient_model.urea = urea
        patient_model.respiratory = respiratory
        patient_model.systolic = systolic
        patient_model.diastolic = diatolic
        patient_model.score = get_score(patient_model)
    
        db.add(patient_model)
        db.commit()

        patients = db.query(models.Patients).all()
        return templates.TemplateResponse("index.html", {"request": request, "patients": patients})
    else:
        message='The patient with ID ' + pid + ' already exists'
        patients = db.query(models.Patients).all()
        return templates.TemplateResponse("index.html", {"request": request, "patients": patients, "message": message})


@app.post("/test")
def new_pat(pat: Patient):
   
    score = get_score(pat)

    return score


@app.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):

    patient_model = db.query(models.Patients).filter(models.Patients.patientId == patient_id).first()

    if patient_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} Does not exist"
        )

    db.query(models.Patients).filter(models.Patients.patientId == patient_id).delete()

    db.commit()


if __name__ == '__main__':
    uvicorn.run(app)