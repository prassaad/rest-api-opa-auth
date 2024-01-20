from fastapi import FastAPI, Security, HTTPException
from utils import VerifyToken
from models import TrainingPayload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth = VerifyToken() # type: ignore

training_list: dict[int, TrainingPayload] = {}

@app.get("/whoami")
def whoami():
    return {"email":"prasada@gmail.com"}

@app.get("/healthcheck/")
def healthcheck():
    return 'Health - OK'

@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result


@app.get("/api/external")
def private(auth_result: str = Security(auth.verify)):
    """A valid access token is required to access this route"""
    return auth_result


@app.get("/api/private-scoped")
def private_scoped(auth_result: str = Security(auth.verify, scopes=['read:messages'])):
    """A valid access token and an appropriate scope are required to access
    this route
    """

    return auth_result

@app.post("/trainings/create")
async def create_training(training : TrainingPayload)  -> dict[str, str]:
    if training is None :
        raise HTTPException(status_code=400, detail="training data must be entred.")
    training_ids: dict[str, int] = {trng.training_name : trng.training_id if trng.training_id is not None else 0 for trng in training_list.values() }
    if training.training_name in training_ids.keys():
        training_id = training_ids[training.training_name]
    else : 
        training_id = max(training_list.keys())+1 if training_list else 0 
        training_list[training_id] = training
    return {"message":"Training added successfully"}

@app.post("/trainings")
async def list_trainings() -> dict[str, dict[int,TrainingPayload]]:
    return {"trainings" : training_list}
