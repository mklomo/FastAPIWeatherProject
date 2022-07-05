"""
    This file contains the implementation logic for the weather api
"""
from typing import Optional

import fastapi
from fastapi import Depends
from models.location import Location
from models.validation import ValidationError
from models.reports import ReportSubmittal, Report
from services.openweather_services import get_report_async
from services.report_service import get_reports, add_report
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from typing import List

# Implement the router
router = fastapi.APIRouter()


# Get the HTML Templates
templates = Jinja2Templates(directory="templates")


# City here is a required path
@router.get("/api/weather/{city}")
async def weather(
    loc: Location = Depends(),
    units: Optional[str] = "metric",
):
    """_summary_: This is the Weather route of the api
    units (optional): The units to get the weather in. Default is metric
    """
    try:
        # Get the response from the async function
        report = await get_report_async(
            city=loc.city, state=loc.state, country=loc.country, units=units
        )
        return report
    except ValidationError as ve:
        return fastapi.Response(content=ve.err_msg, status_code=ve.status_code)
    except Exception as e:
        print("Server Crashed while processing the request: {ve}}")
        return fastapi.Response(
            content="Error processing your request.", status_code=500
        )



# Get all reports
@router.get('/api/reports', name="all_reports", response_model=List[Report])
async def reports_get():
    # Add reports to see how it looks
    # await add_report("Test Report", Location(city="Test City 1", state="Test State 1"))
    # await add_report("Test Report 2", Location(city="Test City 2", state="Test State 2"))
    # Return a list of reports
    return await get_reports()


@router.post('/api/reports', name="add_report", status_code=201, response_model=Report)
async def reports_post(report_submittal: ReportSubmittal):
    desc = report_submittal.description
    loc = report_submittal.location
    return await add_report(desc, loc)