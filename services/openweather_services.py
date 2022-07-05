from typing import Optional
import httpx
from infrastructure.weather_cache import get_weather, set_weather
from models.validation import ValidationError

api_key: Optional[str] = None

async def get_report_async(city, state: Optional[str], country: Optional[str], units: Optional[str]):
    # Validate the parameters
    city, state, country, units = validate_params(city, state, country, units)
    
    if forecast := get_weather(city, state, country, units):
        return forecast
    
    # What happens if the state in None
    if state:
        # Get the URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}"
    
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}"
    
    async with httpx.AsyncClient() as client:
        # Get the response as a co-routine
        response = await client.get(url)
        if response.status_code != 200:
            raise ValidationError(err_msg= response.text, status_code= response.status_code)
    
    # Convert the response to a Python Dictionary or JSON (from Text)
    data = response.json()
    
    # Grab the forecast
    forecast = data["main"]
    
    # Set the forecast in the cache
    set_weather(city, state, country, units, forecast)
    
    return forecast
   
   
def validate_params(city: str, state: Optional[str], country: Optional[str], units: str):
    
    # Validating the city parameter
    city = city.lower().strip()
   
    if not country:
       country = "us"
       
    else:
       country = country.lower().strip()
       
    # Check the length of the country 
    if len(country) != 2:
        raise ValidationError(err_msg="Country must be 2 characters long", status_code=400)
    
    # Validating state
    if state:
        state = state = state.strip().lower()
        
    if state and len(state) != 2:
       raise ValidationError(err_msg="State must be 2 characters long", status_code=400)
   
    # Validating the units
    if units:
        units = units.strip().lower()
        
    valid_units = {"standard", "imperial", "metric"}
    if units not in valid_units:
        raise ValidationError(err_msg="Units must be one of: standard, imperial, metric", status_code=400)
    
    return city, state, country, units