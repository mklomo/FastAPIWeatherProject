"""
    This file contains the implementation logic for the home page
"""
import fastapi
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from services.report_service import get_reports

# Implement the router
router = fastapi.APIRouter()


# Get the HTML Templates
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index(request: Request):
    """_summary_: This is the Home route of the api"""
    events = await get_reports()
    data = {"request": request, "reported_events": events}
    return templates.TemplateResponse("home/index.html", data)


# For favicons
# @api.get("/favicon.ico")
# def favicon():
#     """_summary_: This is the Favicon route of the api
#     """
#     return fastapi.responses.RedirectResponse("/static/favicon.ico")
