import os

from fastapi import FastAPI
from friday.core.server_config import ConfigManager

app = FastAPI()

# Import your services
from friday.api.python.interpreter import router as python_router
from friday.api.arxiv.arxiv import router as arxiv_router
from friday.api.bing.bing_service import router as bing_router
from friday.api.calculator.calculator import router as calculator_router
from friday.api.chemical.chemical import router as chemical_router
from friday.api.ppt.ppt import router as ppt_router
from friday.api.shell.shell import router as shell_router
from friday.api.database.database import router as db_router
from friday.api.wolfram_alpha.wolfram_alpha import router as wa_router
from friday.api.weather.weather import router as weather_router 
from friday.api.google_calendar.calendar_service import router as calendar_router
from friday.api.gmail.gmail import router as gmail_router
from friday.api.markdown.markdown_service import router as markdown_router

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Incoming request: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            print(f"Request error: {str(e)}")
            raise e from None
        else:
            print(f"Outgoing response: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)

# Create a dictionary that maps service names to their routers
services = {
    "python_executor": python_router,
    "calculator": calculator_router,
    "arxiv": arxiv_router,
    "bing": bing_router,
    "chemical": chemical_router,
    "ppt": ppt_router,
    "shell": shell_router,
    "database": db_router,
    "wolframalpha": wa_router,
    "weather": weather_router,
    "calendar": calendar_router,
    "gmail": gmail_router,
    "markdown": markdown_router

}

server_list = ["python_executor", "calculator","arxiv","bing","shell","ppt",
               "database","wolframalpha","weather","calendar","gmail","markdown"]

# Include only the routers for the services listed in server_list
for service in server_list:
    if service in services:
        app.include_router(services[service])

# proxy_manager = ConfigManager()
# proxy_manager.apply_proxies()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8079)
