from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/dispatch')
async def dispatch(req: Request):
    return { "message": "Hello router" }
