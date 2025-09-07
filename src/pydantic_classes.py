from pydantic import BaseModel, ValidationError
from typing import List, Optional

class Action(BaseModel):    
    name: str
    desc: str

class Monster(BaseModel):
    name: str
    hit_points: int
    armor_class: Optional[int] 
    actions: List[Action]