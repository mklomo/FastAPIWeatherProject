from typing import List
from models.location import Location
from models.reports import Report
import datetime as dt
import uuid


__reports: List[Report] = []


async def get_reports():

    # WoulD be async here to get the reports from the DB
    return list(__reports)


async def add_report(description: str, location: Location):
    # Capture now
    now = dt.datetime.now()
    report = Report(
                    id = str(uuid.uuid4()), 
                    description = description, 
                    location = location, 
                    created_date=now)
    # Simulate saving to the database
    # Would be async here
    __reports.append(report)
    # Sort the reports
    __reports.sort(key=lambda r: r.created_date, reverse=True)
    return report
