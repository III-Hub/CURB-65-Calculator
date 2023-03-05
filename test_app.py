from fastapi.testclient import TestClient
from fastapi import status
from app import app
import models

client=TestClient(app=app)

def test_correct_score():
    
    patientId = 'P000001'
    dob = '1939-03-08'
    confusion = 1
    urea = 34
    respiratory = 35
    systolic = 23
    diatolic = 34
    
    response = client.post('/test', json={"patientId":patientId,"dob":dob,"comfusion":confusion,"urea":urea,"respiratory":respiratory,"systolic":systolic,"diatolic":diatolic})
    print(response)
    assert response.json() == {"score": 4}