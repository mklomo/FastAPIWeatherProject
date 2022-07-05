from fastapi import Depends
from pydantic import BaseModel
from typing import Optional

# Creating a Pydantic model for the location
class Location(BaseModel):
    """
    This class is used to define the location
    """

    city: str
    state: Optional[str] = None
    country: Optional[str] = "US"
