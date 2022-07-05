from pydantic import BaseModel
from models.location import Location
import datetime as dt
from typing import Optional

# What users Submit
class ReportSubmittal(BaseModel):
    description: str
    location: Location


class Report(ReportSubmittal):
    id: str
    created_date: Optional[dt.datetime]
    