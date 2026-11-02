from fastapi import FastAPI
import joblib
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Student Placement Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

artifacts = joblib.load("artifacts/placement_model.pkl")

model = artifacts["model"]
scaler = artifacts["scaler"]
feature_columns = artifacts["feature_columns"]

class studentdata(BaseModel):
    gender: str
    branch: str
    city: str
    internship: str
    has_backlog: str

    attendance_percent: float = Field(ge=0, le=100)
    communication_skill: float = Field(ge=0, le=10)
    tech_events_attended: int = Field(ge=0)
    salary_expectation: float = Field(ge=0)
    cgpa: float = Field(ge=0, le=10)
    coding_problems_solved: int = Field(ge=0)

@app.get("/")
def home():
    return "Welcome to our Placement Predictor"

@app.post("/predict")
def predict(data : studentdata):
    student_data = data.model_dump()
    
    from model import prepare_new_student
    
    encoded_data = prepare_new_student(student_data, feature_columns)
    
    scaled_data = scaler.transform(encoded_data)
    
    prediction = int(model.predict(scaled_data)[0])
    
    probability = float(model.predict_proba(scaled_data)[0][1])
    
    
    return {
        "prediction" : prediction,
        "result" : "placed" if prediction==1 else "not placed",
        "probability": round(probability, 4)
        
    }