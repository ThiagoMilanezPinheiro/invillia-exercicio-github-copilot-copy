"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Esportivas
    "Soccer Team": {
        "description": "Treinos e competições de futebol para representar a escola",
        "schedule": "Segundas e Quartas, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "maria@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Treinos de basquete e participação em campeonatos inter-escolares",
        "schedule": "Terças e Quintas, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
    },
    # Artísticas
    "Art Club": {
        "description": "Exploração de técnicas de desenho, pintura e artes plásticas",
        "schedule": "Quartas, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Prática instrumental e vocal para apresentações escolares",
        "schedule": "Sextas, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "ava@mergington.edu"]
    },
    # Intelectuais
    "Debate Team": {
        "description": "Desenvolver habilidades de argumentação e participar de torneios de debate",
        "schedule": "Segundas, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu", "harper@mergington.edu"]
    },
    "Science Club": {
        "description": "Experimentos, projetos científicos e feiras de ciências",
        "schedule": "Quintas, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu", "sophia.j@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validar se a atividade existe
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validar se o aluno já está inscrito
    normalized_email = email.strip().lower()
    existing = [p.strip().lower() for p in activity["participants"]]
    if normalized_email in existing:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Verificar se há vagas disponíveis
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Adicionar estudante
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
