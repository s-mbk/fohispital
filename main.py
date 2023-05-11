from fastapi import FastAPI
import os
import json

app = FastAPI()

# view patient data

@app.get("/")
async def root():

    files = os.listdir('fhir_resources')

    patients = []
    for filename in files:
        with open(f"fhir_resources/{filename}") as file:
            patients.append(json.load(file))

    return patients


# add new patient data

@app.post("/patients/create")
async def patient_create(jsonData):
    # How to secure our "post-box"?
    # Check for valid JSON
    try:
        patient = json.loads(jsonData)
    except ValueError as err:
        return False

    # TODO: Check header for the right Content-Type: application/json+fhir
    
    # Giving the newly created file (patient) a file name (patient id) in continuation of already existing files (patient ids)
    file_id = len(os.listdir('fhir_resources')) + 1
    filename = f"patient_{file_id}.json"

    with open(filename, 'w') as file:
        json.dump(patient, file)
        # json.dump() converts the Python objects into appropriate json objects

    return 'OK'
    
