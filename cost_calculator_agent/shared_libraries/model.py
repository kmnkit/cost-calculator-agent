from pydantic import BaseModel, Field
from typing import Optional

class Service(BaseModel):
    name: str = Field(..., description='AWS Service')
    reason: str = Field(..., description='The reason why this service chosen')
    
class Architecture(BaseModel):
    services: list[Service]
