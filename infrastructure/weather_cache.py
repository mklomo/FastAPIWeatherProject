"""
    This file contains the in-memory cacheing implementation for the weather api
"""


import datetime
from typing import Optional, Tuple

__cache = {}
lifetime_in_hours = 1.0


def get_weather(
    city: str, state: Optional[str], country: Optional[str], units: Optional[str]
):
    """_summary_: This is the Weather route of the api
    units (optional): The units to get the weather in. Default is metric
    """
    # Get the response from the async function
    key = __create_key(city, state, country, units)
    data: dict = __cache.get(key)
    # What happens if there is not data
    if not data:
        # Return none
        return None

    # Get the last time the same key was used
    last = data["time"]
    # Check if the same request was made less than an hour ago
    dt = datetime.datetime.now() - last

    if dt / datetime.timedelta(minutes=60) < lifetime_in_hours:
        # Remove the data
        return data["value"]

    del __cache[key]
    return None


def set_weather(city: str, state: str, country: str, units: str, value: dict):
    key = __create_key(city, state, country, units)
    data = {"time": datetime.datetime.now(), "value": value}
    __cache[key] = data
    __clean_out_of_date()


def __create_key(city: str, state: str, country: str, units: str):
    if not city or not country or not units:
        raise Exception("City, State, Country, and Units are required")
    # state can be optional
    if not state:
        state = ""

    return (
        city.strip().lower(),
        state.strip().lower(),
        country.strip().lower(),
        units.strip().lower(),
    )


def __clean_out_of_date():
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get("time")
        if dt / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]
