import asyncio
from imp import reload
import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather_api
from views import home
from pathlib import Path
import json
from services import report_service, openweather_services
from models.location import Location
import nest_asyncio


api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()


def configure_api_keys():
    file = Path("settings.json").absolute()
    if not file.exists():
        print(
            f"WARNING: {file} does not exist. Please see settings_template.json for an example."
        )
        raise Exception(
            "settings.json does not exist. Please see settings_template.json for an example."
        )

    with open("settings.json") as f:
        settings = json.load(f)
        openweather_services.api_key = settings.get("api_key")


def configure_routing():
    # Opt in Styling by mounting the styles
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(home.router, tags=["home"])
    api.include_router(weather_api.router, tags=["weather"])



if __name__ == "__main__":
    configure()
    uvicorn.run("main:api", reload=True)
    

else:
    configure()

