from fastapi import FastAPI
from .router import app as router_app
from .system import app as system_app

app = FastAPI()
app.mount('/router', router_app)
app.mount('/system', system_app)
