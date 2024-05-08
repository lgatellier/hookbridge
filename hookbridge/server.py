import uvicorn


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("hookbridge.main:app", host="0.0.0.0", port=8000, reload=True)
