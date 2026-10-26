
lookup_weather_schema = {
    "type":"function",
    "function" : {
        "name": "lookup_weather",
        "description": (
            "look up current, live weather for a place using Open-Meteo API. "
            "Use this whenever the user asks for the weather in a location, or for wind speed, sky condition or temperature"
        ),
        "parameters":{
            "type":"object",
            "properties":{
                "location":{
                    "type":"string",
                    "description": "The name of the location to look up the weather for eg 'Lucknow', 'London'"
                }
            },
            "required":["location"],
        }
    }
}

TOOL_MENU = [lookup_weather_schema]

def tool_catalog()->list[dict[str,str]]:
    return [
        {
            "name":tool["function"]["name"],
            "description": tool["function"]["description"]
        }for tool in TOOL_MENU
    ]