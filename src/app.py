""" Server-side application. Contains various endpoints to record and return. """
""" For a single user. """
from fastapi import FastAPI
from pydantic import BaseModel

from name_recognizer import NameClassifier

app = FastAPI()

class Sender(BaseModel):
    sender: str

@app.get("/") # Root
def root():
    return "Go to /docs for the docs"

@app.get("/fetch_emails")
async def fetch_emails_prototype():
    """ Fetch the emails, 50 at a time (Gmail application limit) """

