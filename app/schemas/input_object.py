from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class InputObjectBase(BaseModel):
    pass
    # *****************************************
    # Add Attributes Here
    # *****************************************

class InputObject(InputObjectBase):
    class Config:
        orm_mode = True
