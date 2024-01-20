from typing import Optional
from pydantic import BaseModel

class TrainingPayload(BaseModel):
    training_id : Optional[int]
    training_type : str
    training_model : str
    training_name : str
    training_state : int
