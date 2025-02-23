from fastapi import FastAPI
from controller import llmController

app = FastAPI()

app.include_router(llmController.router)
